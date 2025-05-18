from utils.ModelActor import *
import json
from utils.Searcher import *
import time
from threading import Thread
from queue import Queue

num_of_searchers = 32

threads_of_searchers = 32

search_pool = SearcherPool()
for i in range(num_of_searchers):
    search_pool.push(Searcher(model_pool=None))
def get_start0(theorem_list,flag=True):
    new_theorem_list = []
    for i in theorem_list:
        name = i.name
        idx = name.find("__")
        if name[idx+2]=='0':
            if flag:new_theorem_list.append(i)
        else:
            if not flag:new_theorem_list.append(i)
    return new_theorem_list
def repair_theorem(theorem:MyTheorem,neg=False) -> MyTheorem:
    current_theorem = copy.deepcopy(theorem)
    current_theorem.goal = repair(current_theorem.goal,neg)
    current_theorem.primises = [repair(line,neg) for line in current_theorem.primises]
    return current_theorem
def correct_single_theorem(tasks, output_success_dir,output_failure_dir):
    print(len(tasks))
    for i in tasks:
        i.correct = None
    tasks_queue = Queue()
    for v in tasks:
        tasks_queue.put(v)
    all_results = []
    threads = []
    def worker():
        while not tasks_queue.empty():
            task = tasks_queue.get()
            # print("task submit:", task)
            results = search_pool.submit(lambda a, v: a.corrector(v), task)
            all_results.append(results)
    for i in range(threads_of_searchers):
        t = Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    correct_list=[]
    failure_list=[]
    for i in all_results:
        if i.is_correct():correct_list.append(i.to_json())
        else: failure_list.append(i.to_json())
    json.dump(correct_list, fp=output_success_dir.open("w") ,ensure_ascii=False, indent=2)
    json.dump(failure_list, fp=output_failure_dir.open("w"), ensure_ascii=False, indent=2)

if __name__=="__main__":
    # The path of the searched folder should include the common subfolders
    input_dir = ""

    common_dir=os.path.join(input_dir,"common")
    success_dir=Path(input_dir,"success")
    failure_dir=Path(input_dir,"failure")
    for name in os.listdir(common_dir):
        print(name)
        output_success_dir=Path(success_dir,name)
        output_failure_dir=Path(failure_dir,name)
        output_common_dir=Path(common_dir,name)
        if  output_success_dir.exists() and (len(json.load(output_success_dir.open('r'))) > 0 or len(json.load(output_failure_dir.open('r'))) > 0): continue
        with open(output_common_dir) as f:
            dic_list = json.load(f)
        theorem_list = []
        for i in dic_list:
            theorem = MyTheorem()
            theorem.load_from_json(i)
            theorem_list.append(theorem)
        try:
            correct_single_theorem(theorem_list,output_success_dir,output_failure_dir)
        except Exception as e:
            continue