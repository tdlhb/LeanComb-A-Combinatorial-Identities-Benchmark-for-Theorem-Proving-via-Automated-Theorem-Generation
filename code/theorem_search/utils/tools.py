from utils.Constant import *
from utils.ModelActor import *
from utils.MyTheorem import *
import json
from utils.Searcher import *
import time
from threading import Thread
from queue import Queue
from utils.repair import *

def process_primise(primise:str):
    return primise.split("\n")
def repair_theorem(theorem:MyTheorem,neg=False) -> MyTheorem:

    current_theorem = copy.deepcopy(theorem)
    current_theorem.goal = repair(current_theorem.goal,neg)
    current_theorem.primises = [repair(line,neg) for line in current_theorem.primises]
    return current_theorem
def exact_sigle_theorem(json_item:dict):
    if "infotree" not in json_item.keys(): return []

    if len(json_item["infotree"]) == 0: return []
    theorem_list = []
    work_dir = LEAN_WORKDIR
    file_path = json_item["file_path"]
    
    theorem_name = os.path.splitext(json_item["leanfilename"])[0]
    init_state = json_item["infotree"][0]["node"]["goalsBefore"][0] 

    primise, goal = init_state.split("⊢") 

    primise = process_primise(primise) 
    
    theorem_len = len(json_item["infotree"])


    start_pos = 0
    tactic_list = []
    new_theorem = MyTheorem()
    new_theorem.name = theorem_name + f"__0__0__{theorem_len}"
    new_theorem.primises = primise
    new_theorem.goal = goal.replace("-1", "(-1:ℝ)")
    new_theorem.tactics = []
    new_theorem.project_dir = work_dir
    new_theorem.file_path = file_path
    theorem_list.append(new_theorem)
    theorem_list.append(repair_theorem(new_theorem))
    for end_pos in range(start_pos, theorem_len):
        start_node = json_item["infotree"][start_pos]["node"]
        end_node = json_item["infotree"][end_pos]["node"]
        tactic_list.append(end_node["stx"]["pp"])
        new_theorem = MyTheorem()
        new_theorem.name = theorem_name + f"__{start_pos}__{end_pos+1}__{theorem_len}"
        new_theorem.primises = process_primise((start_node["goalsBefore"][0]).split("⊢")[0])
        goal = (start_node["goalsBefore"][0]).split("⊢")[1]
        new_theorem.goal = goal.replace("-1", "(-1:ℝ)")
        
        new_theorem.tactics = copy.deepcopy(tactic_list)
        new_theorem.project_dir = work_dir
        new_theorem.file_path = file_path
        theorem_list.append(new_theorem)
        theorem_list.append(repair_theorem(new_theorem))

    return theorem_list

def bfs_single_theorem(json_file_path):
    with open(json_file_path, 'r') as file:
        json_content = json.load(file)
    if json_content == None: return
    result = exact_sigle_theorem(json_content)
    return result
def get_alltactic(theorem:MyTheorem) -> list:
    theorem_list = []
    for i in range(len(theorem.tactics)):
        new_theorem = copy.deepcopy(theorem)
        new_theorem.tactics = new_theorem.tactics[:i+1]
        theorem_list.append(new_theorem)
    return theorem_list
