from utils.Constant import *
from utils.lean4Kit.Lean4Kit import *
import heapq
import time
from threading import Lock
from utils.MyTheorem import MyTheorem
from queue import Queue
import copy
from utils.repair import *
from utils.Searcher_alphazero import *
from utils.model import *


class SearcherPool:
    def __init__(self) -> None:
        self.searchers = []
        self.searchers_status = []
        self.lock = Lock()

    def push(self, searcher):
        self.searchers.append(searcher)
        self.searchers_status.append(True)

    def submit(self, fn, val):
        idx = 0
        while True:
            with self.lock:
                if self.searchers_status[idx]:
                    self.searchers_status[idx] = False
                    break
                idx = (idx + 1) % len(self.searchers)
        if VERBOSE:
            print("task submitted to searcher")
        results = fn(self.searchers[idx], val)
        with self.lock:
            self.searchers_status[idx] = True
        return results


class Searcher:
    def __init__(self, model_pool, time_out=600, max_iters=10**6, queue_max_count=10**6) -> None:
        self.lean = None
        self.time_out = time_out
        self.max_iters = max_iters
        self.queue_max_count = queue_max_count
        self.model_pool = model_pool
    def repair_theorem(self,theorem:MyTheorem,neg=False) -> MyTheorem:
            current_theorem = copy.deepcopy(theorem)
            current_theorem.goal = repair(current_theorem.goal,neg)
            current_theorem.primises = [repair(line,neg) for line in current_theorem.primises]
            return current_theorem
    def eval(self, theorem) -> list:
        try:
            self.lean = Lean4Kit(LEAN_WORKDIR, REPL_VERSION, verbose=True)
            state = self.lean.new_thm(theorem, verbose=True)
        except Exception as e:
            self.lean.close()
            print(e)
            print(theorem)
            return []

        print("Theorem init success")
        visited = set([state.getTacticState()])
        sta_queue = [(0.0, [], state)]
        # proof_finished = False

        start_time = time.time()
        for _ in range(self.max_iters):
            if len(sta_queue) == 0:
                self.lean.close()
                print("queue is empty or proof is finished")
                break
            current_time = time.time()
            if current_time - start_time > self.time_out or len(sta_queue) > self.queue_max_count:
                self.lean.close()
                print("theorem is not proved")
                break

            score, steps, state_now = heapq.heappop(sta_queue)
            res = self.model_pool.submit(lambda a, v: a.generate_tactics_scores.remote(*v),
                                         (state_now.getTacticState(), SAMPLE_CONFIG))
            for txt, sce in res:
                try:
                    new_state = self.lean.run_tactic(
                        txt, state_now.proofStates[0], verbose=True)
                except Exception as e:
                    print("Tactic run failed")
                    continue
                if new_state.isError():
                    print("Tactic apply failed")
                    continue
                elif new_state.isFinish():
                    try:
                        if self.lean.is_correct_and_finished(theorem+" := by\n"+'\n'.join(steps+[txt])):
                            self.lean.close()
                            print("Theorem is proved")
                            # proof_finished = True
                            print("search finished")
                            return steps + [txt]
                        else:
                            print("Theorem is not proved")
                            continue
                    except Exception as e:
                        continue
                elif new_state.getTacticState() in visited:
                    continue
                visited.add(new_state.getTacticState())
                heapq.heappush(
                    sta_queue, (score - sce , steps + [txt], new_state))
        self.lean.close()
        print("Search failed")
        return []
    def corrector(self,theorem:MyTheorem, new_primise_name:str="h"):
        _repair_theorem = self.repair_theorem(theorem)
        correct_theorem = copy.deepcopy(theorem)
        if theorem.is_correct(): return copy.deepcopy(theorem)
        if _repair_theorem.__str__()!=correct_theorem.__str__() and  _repair_theorem.is_correct():return _repair_theorem
        lean = Lean4Kit(LEAN_WORKDIR,REPL_VERSION,verbose=VERBOSE)
        try:
            current_state = lean.new_thm(theorem._code(),verbose=VERBOSE)
            for _tactic in theorem.tactics:
                if current_state.isFinish() and not current_state.isError():break
                if current_state.isError()==True:
                    correct_theorem.is_correct()
                    return correct_theorem
                current_state = lean.run_tactic(_tactic,current_state.proofStates[0])
        except Exception as ex:
            lean.close()
            correct_theorem.is_correct()
            return correct_theorem
        lean.close()
        if current_state.getTacticState() == None:
            correct_theorem.is_correct()
            return correct_theorem
        
        if current_state.getTacticState().count("⊢") != 1:
            correct_theorem.is_correct()
            return correct_theorem
        
        new_tactics = []

        if current_state.getTacticState() != "no goals" :
            goal = current_state.getTacticState().split("⊢")[-1]
            tmp_goal = correct_theorem.goal.replace(" ","").replace("↑","").replace("(","").replace(")","").replace(":","").replace("ℝ","")
            tmp_primises = goal.replace(" ","").replace("↑","").replace("(","").replace(")","").replace(":","").replace("ℝ","")
            if tmp_goal == tmp_primises:
                correct_theorem.is_correct()
                return correct_theorem
            correct_theorem.primises.append(f"{new_primise_name}: {correct_theorem.goal}")
            correct_theorem.goal = goal

        correct_theorem.goal = correct_theorem.goal.replace("(-1)", "(-1:ℝ)")
        def process_tactic(tactic:str):
            tactic = tactic.strip()
            if tactic.startswith("rw") or tactic.startswith("simp"):
                if tactic.count(" at ") != 0:
                    return tactic
                else:
                    if tactic.count("\n"): tactic = tactic.split("\n")[0]
                    return tactic + f" at {new_primise_name}" 
            else:
                return tactic
        for _tactic in correct_theorem.tactics:
            new_tactics.append(process_tactic(_tactic))

        new_tactics.append("assumption")
        correct_theorem.correct = None
        correct_theorem.tactics = new_tactics
        repair_theorem_assumption = self.repair_theorem(correct_theorem)
        correct = correct_theorem.is_correct()
        if correct:return correct_theorem
        if repair_theorem_assumption.__str__()!=correct_theorem.__str__() and  repair_theorem_assumption.is_correct():return repair_theorem_assumption
        return correct_theorem  
    def alphazero_search(self, theorem: MyTheorem):
        code = theorem._code()
        steps = theorem.tactics
        tactic_list = []
        
        # Initialize models
        feature_size = 100
        policymodel = policy_model(feature_size*2)
        valuemodel = value_model(feature_size)
        
        # Load trained models
        checkpoint_policy = torch.load(POLICY_MODEL_PATH)
        policymodel.load_state_dict(checkpoint_policy['state_dict'])
        
        checkpoint_value = torch.load(VALUE_MODEL_PATH)
        valuemodel.load_state_dict(checkpoint_value['state_dict'])
        
        # Initialize Lean
        lean = Lean4Kit(LEAN_WORKDIR, REPL_VERSION, VERBOSE)
        visited_states = set()
        try:
            state = lean.new_thm(code, verbose=VERBOSE)
            visited_states.add(state.getTacticState())
        except:
            lean.close()
            return None
        
        # Apply initial tactics if any
        for step in steps:
            tactic_list.append(step)
            try:
                state = lean.run_tactic(step, state.proofStates[0], verbose=VERBOSE)
                if state.isError() or state.isFinish():
                    break
                visited_states.add(state.getTacticState())
            except:
                lean.close()
                return None
        
        if state.isFinish():
            new_theorem = deepcopy(theorem)
            new_theorem.tactics = tactic_list
            new_theorem.correct = True
            lean.close()
            return [new_theorem]
        
        # Create root state and run AlphaZero MCTS
        root_state = AlphaZeroState(state, "", tactic_list, len(tactic_list), lean, self.model_pool,visited_states=visited_states)
        mcts = AlphaZeroMCTS(root_state, policymodel, valuemodel, self.model_pool, 300)
        all_path = mcts.all_action()
        
        # Prepare results
        theorem_list = []
        for path in all_path:
            new_theorem = deepcopy(theorem)
            new_theorem.tactics = path
            new_theorem.correct = False
            theorem_list.append(new_theorem)
        
        lean.close()
        return theorem_list