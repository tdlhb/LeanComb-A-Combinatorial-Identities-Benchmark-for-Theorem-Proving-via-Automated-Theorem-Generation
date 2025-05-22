from utils.Constant import *
import math
import random
import time
import numpy as np
from ray.util import ActorPool
from utils.ModelActor import *
from utils.lean4Kit.Lean4Kit import *
from utils.lean4Kit.LeanKitException import *
from copy import deepcopy
import torch
from collections import defaultdict

class AlphaZeroState:
    def __init__(self, proof_state: TacticState, formal_theorem, history_tactics, depth, 
                 lean: Lean4Kit, model_actor_pool: ModelActorPool, visited_states=None):
        self.proof_state = proof_state
        self.formal_theorem = formal_theorem
        self.history_tactics = history_tactics
        self.depth = depth
        self.lean = lean
        self.model_actor_pool = model_actor_pool
        self.children = []
        self.possible_actions = None
        self.actions_scores = []
        self._encoded_state = None
        self.visited_states = visited_states if visited_states is not None else set()
        
        # Add current state to visited set if it exists
        if proof_state is not None:
            state_str = proof_state.getTacticState()
            self.visited_states = self.visited_states.copy()  # Create a new copy for this branch
            self.visited_states.add(state_str)

    def encode_state(self):
        """Encode the current state for neural network input"""
        if self._encoded_state is None:
            tactic_state = self.proof_state.getTacticState() if self.proof_state else ""
            self._encoded_state = self.model_actor_pool.submit(
                lambda a, v: a.encode_tactic_state.remote(v),
                tactic_state
            )
        return self._encoded_state

    def is_terminal(self):
        return (self.depth > MCTS_MAX_DEPTH or
                self.proof_state is None or
                self.proof_state.isFinish() or 
                self.proof_state.isError() or
                len(self.get_possible_actions()) == 0)

    def get_possible_actions(self):
        if self.possible_actions is not None:
            return self.possible_actions


        model_input = self.proof_state.getTacticState()
        input_text = self.model_actor_pool.submit(
            lambda a, v: a.get_model_input.remote(v),
            model_input
        )
        
        response = self.model_actor_pool.submit(
            lambda a, v: a.generate.remote(v),
            input_text
        )

        texts, scores = [], []
        for output in response[0].outputs:
            if output.text not in texts:
                try:
                    texts.append(output.text)
                    scores.append(0)
                except Exception:
                    continue

        self.possible_actions = texts
        self.actions_scores = scores
        return self.possible_actions

    def generate_child(self, action):
        try:
            new_state = self.lean.run_tactic(action, self.proof_state.proofStates[0], verbose=VERBOSE)
        except Exception:
            new_state = None

        if new_state is not None:
            new_state_str = new_state.getTacticState()
            if new_state_str in self.visited_states:
                return None  # Skip duplicate states

        return AlphaZeroState(
            new_state,
            self.formal_theorem,
            deepcopy(self.history_tactics) + [action],
            self.depth + 1,
            self.lean,
            self.model_actor_pool,
            self.visited_states  # Pass along the visited states
        )

    def get_reward(self):
        if self.proof_state is None:
            return -1
        if self.proof_state.isFinish() and not self.proof_state.isError():
            proof_complete = self.lean.is_correct_and_finished(
                self.formal_theorem + "\n" + "\n".join(self.history_tactics)
            )
            return 1 if proof_complete else -1
        return -1

class AlphaZeroNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value_sum = 0.0
        self.prior = 0.0  # Prior probability from policy network
    
    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_possible_actions())
    
    def best_child(self, exploration_constant=1.0):
        best_score = -float('inf')
        best_child = None
        
        for child in self.children:
            if child.visits == 0:
                ucb = float('inf')
            else:
                # AlphaZero's modified UCB formula
                ucb = (child.value_sum / child.visits) + \
                     exploration_constant * child.prior * math.sqrt(self.visits) / (child.visits + 1)
            
            if ucb > best_score:
                best_score = ucb
                best_child = child
                
        return best_child
    
    def add_child(self, child, prior):
        if child is not None:  # Only add non-None children (filtered duplicates)
            child.prior = prior
            self.children.append(child)
            child.parent = self

class AlphaZeroMCTS:
    def __init__(self, root_state, policy_model, value_model, model_actor_pool, search_time_budget=SEARCH_TIME_BUDGET):
        self.root = AlphaZeroNode(root_state)
        self.policy_model = policy_model
        self.value_model = value_model
        self.model_actor_pool = model_actor_pool
        self.search_time_budget = search_time_budget
    
    # def simulate(self, state):
    #     while not state.is_terminal():
    #         actions = state.get_possible_actions()
    #         if not actions:
    #             break
    #         # Try actions until we find one that doesn't create a duplicate state
    #         for action in random.sample(actions, len(actions)):
    #             new_state = state.generate_child(action)
    #             if new_state is not None:  # Found a non-duplicate state
    #                 state = new_state
    #                 break
    #         else:  # All actions lead to duplicate states
    #             break
    #     return state, state.get_reward() if state is not None else (None, -1)
    def simulate(self, state):
        visited_in_path = set()
        if state.proof_state is not None:
            visited_in_path.add(state.proof_state.getTacticState())
        
        while not state.is_terminal():
            actions = state.get_possible_actions()
            if not actions:
                break
                
            # Try actions in random order
            for action in random.sample(actions, len(actions)):
                try:
                    new_proof_state = state.lean.run_tactic(action, state.proof_state.proofStates[0], verbose=VERBOSE)
                    if new_proof_state is None:
                        continue
                        
                    new_state_str = new_proof_state.getTacticState()
                    if new_state_str in visited_in_path:
                        continue  # Skip duplicate states
                        
                    # Found valid non-duplicate state
                    visited_in_path.add(new_state_str)
                    state = AlphaZeroState(
                        new_proof_state,
                        state.formal_theorem,
                        deepcopy(state.history_tactics) + [action],
                        state.depth + 1,
                        state.lean,
                        state.model_actor_pool
                    )
                    break
                except Exception:
                    continue
            else:
                # All actions either failed or led to duplicate states
                break
                
        return state, state.get_reward() if state is not None else (None, -1)
    def expand(self, node):
        if node.state.is_terminal():
            return node
        
        # Get policy predictions for all possible actions
        state_encoding = node.state.encode_state()
        action_probs = {}
        possible_actions = node.state.get_possible_actions()
        
        for action in possible_actions:
            try:
                # Encode the action
                action_encoding = self.model_actor_pool.submit(
                    lambda a, v: a.encode_tactic_state.remote(v),
                    action
                )
                
                # Combine state and action for policy prediction
                combined = np.concatenate([state_encoding, action_encoding])
                action_prob = self.policy_model.predict(combined)
                action_probs[action] = action_prob
            except:
                action_probs[action] = 0.0
        
        # Normalize probabilities
        total = sum(action_probs.values())
        if total > 0:
            action_probs = {k: v/total for k, v in action_probs.items()}
        
        # Create child nodes with prior probabilities, skipping duplicates
        expanded_any = False
        for action, prior in action_probs.items():
            child_state = node.state.generate_child(action)
            if child_state is not None:  # Only create node if state is not duplicate
                child_node = AlphaZeroNode(child_state, node)
                node.add_child(child_node, prior)
                expanded_any = True
        
        return node.children[0] if expanded_any else None
    
    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value_sum += reward
            node = node.parent
    
    def tree_policy(self, node):
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                expanded_node = self.expand(node)
                if expanded_node is None:  # Couldn't expand (all duplicates)
                    break
                return expanded_node
            else:
                node = node.best_child()
                if node is None:  # No valid children
                    break
        return node
    
    def best_action(self, simulations=500, tqdm=False):
        start_time = time.time()
        
        for _ in trange(simulations, leave=False) if tqdm else range(simulations):
            current_time = time.time()
            if current_time - start_time > self.search_time_budget:
                break
            
            # Selection and Expansion
            node = self.tree_policy(self.root)
            if node is None:
                continue
                
            # Evaluation
            if node.state.is_terminal():
                reward = node.state.get_reward()
            else:
                # Get value estimate from neural network
                state_encoding = node.state.encode_state()
                reward = self.value_model.predict(state_encoding)
            
            # Backpropagation
            self.backpropagate(node, reward)
            
            if node.state.is_terminal() and reward > 0:
                print("Theorem proved successfully")
                return node.state.history_tactics
        
        return []
    
    def all_action(self, simulations=500, tqdm=False):
        start_time = time.time()
        
        for _ in trange(simulations, leave=False) if tqdm else range(simulations):
            current_time = time.time()
            if current_time - start_time > self.search_time_budget:
                break
            
            # Selection and Expansion
            node = self.tree_policy(self.root)
            if node is None:
                continue
                
            # Evaluation
            if node.state.is_terminal():
                reward = node.state.get_reward()
            else:
                state_encoding = node.state.encode_state()
                reward = self.value_model.predict(np.array(state_encoding, dtype=np.float32))
            
            # Backpropagation
            self.backpropagate(node, reward)
        
        # Collect all explored paths
        all_actions = []
        def dfs(node, current_path):
            if not node.children:
                full_path = node.state.history_tactics if node.state else []
                if full_path:  # Only add non-empty paths
                    all_actions.append(full_path)
            else:
                for child in node.children:
                    dfs(child, current_path)
        
        dfs(self.root, [])
        
        print(f"Found {len(all_actions)} unique action sequences")
        return all_actions