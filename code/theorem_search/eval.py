from utils.ModelActor import *
import json
from utils.Searcher import *
import time
from threading import Thread
from queue import Queue

num_of_actors = 1

num_of_searchers = 1

threads_of_searchers = 1
model_actors = ModelActorPool()
for i in range(num_of_actors):
    model_actors.push(ModelActor.remote(VLLM_CONFIG, 
                                            PROMPT_CONFIG,
                                            SAMPLE_CONFIG))
    time.sleep(MODEL_LOAD_GAP)


init_state = """import Theorem\nimport Mathlib
open BigOperators Real Nat Topology
"""

# File for recording test results
record_file = ""

# Test set path
task_file = ""


def get_tasks():
    tasks = []
    visited_theorem = set()

    try:
        with open(record_file, "r") as f:
            for line in f:
                dt = json.loads(line)
                visited_theorem.add(dt["theorem"])
    except FileNotFoundError:
        pass
    with open(task_file, "r") as f:
        for line in f:
            data = json.loads(line)
            theorem = data["formal_statement"]
            theorem = theorem[0:theorem.find(":=")]
            theorem = init_state + theorem
            if theorem in visited_theorem:
                continue
            tasks.append(theorem)
    return tasks

lock = Lock()
#The result is in JSON format and contains three fields: theorem description (theorem), whether the search was successful (results), and if the search was successful (tactics)
def write_record(task, results):
    with lock:
        with open(record_file, "a") as f:
            dt = dict()
            dt["theorem"] = task
            if len(results) > 0:
                dt["results"] = True
                dt["tactics"] = results
            else:
                dt["results"] = False
                dt["tactics"] = []
            f.write(json.dumps(dt) + "\n")

def solve():
    tasks = get_tasks()
    tasks_queue = Queue()
    for v in tasks:
        tasks_queue.put(v)

    search_pool = SearcherPool()
    for i in range(num_of_searchers):
        search_pool.push(Searcher(model_pool=model_actors))
        time.sleep(3)

    threads = []

    def worker():
        while not tasks_queue.empty():
            task = tasks_queue.get()
            print("task submit:", task)
            results = search_pool.submit(lambda a, v: a.eval(v), task)
            write_record(task, results)
    # worker()
    for i in range(threads_of_searchers):
        t = Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__ == "__main__":
    solve()