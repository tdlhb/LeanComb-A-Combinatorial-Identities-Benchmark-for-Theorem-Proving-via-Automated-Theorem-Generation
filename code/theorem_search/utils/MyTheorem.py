from utils.Constant import *
from utils.lean4Kit.Lean4Kit import Lean4Kit,TacticState
from pathlib import Path



class MyTheorem:
    def __init__(self, name: str = "", primises: list = [], 
                 goal: str = "", tactics: list = [], states: list = [],
                 file_envs: list = []) -> None:
        self.url = None
        self.commit = None
        self.project_dir = None
        self.file_path = None
        self.name = name
        self.primises = primises
        self.goal = goal
        self.tactics = tactics
        self.states = states
        self.file_envs = file_envs
        self.correct = None
        self.num_predict_steps = 0
        self.code = None
        self.all_code = None
    def _code(self,all=False) -> str:
        origin_file_path = Path(LEAN_WORKDIR, self.file_path)
        origin_code = origin_file_path.read_text()
        lines = origin_code.splitlines()
        for index, line in enumerate(lines):
            if line.strip().startswith("theorem"):
                lines = lines[:index]
                break
            if line.strip().startswith("lemma"):
                lines = lines[:index]
                break
        origin_code = "\n".join(lines)+'\n'
        origin_code += "theorem " + self.name
        for primise in self.primises:
            if primise.count(":") >= 1:
                origin_code += ("(" + primise + ")")  
        origin_code += (" :\n  " + self.goal +' ')
        self.code = origin_code
        self.all_code = origin_code + " := by\n"
        for tactic in self.tactics:
            if tactic.strip() != "": 
                for _line in tactic.split("\n"):  
                    self.all_code += ("  " + _line+ "\n")
        self.all_code = "import Theorem\n"+self.all_code
        origin_code = "import Theorem\n"+origin_code  
        if all: return self.all_code
        else: return origin_code
    
    def to_json(self):
        ans = dict()
        ans["url"] = self.url
        ans["commit"] = self.commit
        ans["project_dir"] = self.project_dir
        ans["file_path"] = self.file_path
        ans["name"] = self.name
        ans["primises"] = self.primises
        ans["goal"] = self.goal
        ans["tactics"] = self.tactics
        ans["file_envs"] = self.file_envs
        ans["correct"] = self.correct
        ans["num_predict_steps"] = self.num_predict_steps
        return ans

    def load_from_json(self, json_item:dict):
        if self.url:
            self.url = json_item["url"]
        self.commit = json_item["commit"]
        self.project_dir = json_item["project_dir"]
        self.file_path = json_item["file_path"]
        self.name = json_item["name"]
        self.primises = json_item["primises"]
        self.goal = json_item["goal"]
        self.tactics = json_item["tactics"]
        self.file_envs = json_item["file_envs"]
        self.correct = json_item["correct"]
        self.num_predict_steps = json_item["num_predict_steps"]

    def is_correct(self) -> bool:
        self.num_predict_steps=len(self.tactics)
        if self.correct != None:
            return self.correct
        lean = Lean4Kit(LEAN_WORKDIR,REPL_VERSION,verbose=False)
        # print(self.all_code)
        self.correct = lean.is_correct_and_finished(self._code(all=True),verbose=VERBOSE)
        lean.close()
        return self.correct
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, MyTheorem) and (self.goal == __value.goal):
            if len(self.tactics) != len(__value.tactics): return False
            for i in range(len(self.tactics)):
                if self.tactics[i] != __value.tactics[i]:
                    return False

            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.goal)
    
    def __str__(self) -> str:
        ans = "theorem " + self.name

        for primise in self.primises:
            if primise.count(":") >= 1:
                ans += ("(" + primise + ")")  
        
        ans += (" :\n  " + self.goal + " := by\n")

        for tactic in self.tactics:
            if tactic.strip() != "":

                for _line in tactic.split("\n"):  
                    ans += ("  " + _line + "\n")

        return ans
    
