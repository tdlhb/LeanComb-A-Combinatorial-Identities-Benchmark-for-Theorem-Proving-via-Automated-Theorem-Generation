from utils.Constant import *
from utils.ModelActor import *
from utils.MyTheorem import *
import json
from utils.Searcher import *
import time
from threading import Thread
from queue import Queue
from utils.repair import *
from utils.tools import *
# The number of actors, which refers to the number of models loaded
num_of_mcts = 1
num_of_actors = GPU_AVAILABLE_COUNT
model_actors = ModelActorPool()
for i in range(num_of_actors):
    model_actors.push(ModelActor.remote(VLLM_CONFIG, 
                                        PROMPT_CONFIG,
                                        SAMPLE_CONFIG))
    time.sleep(MODEL_LOAD_GAP)
lock = Lock()
def write_record(ans,output_common_dir):
    with lock:
        json.dump(ans, fp=output_common_dir.open("w"), ensure_ascii=False, indent=2)
def search_single_theorem(file_path, output_dir):
    json_file_path = Path(file_path)
    output_success_dir = Path(output_dir, "success", json_file_path.stem + ".json")
    output_failure_dir = Path(output_dir, "failure", json_file_path.stem + ".json")
    output_common_dir = Path(output_dir, "common", json_file_path.stem + ".json")
    if output_success_dir.exists() and (len(json.load(output_success_dir.open('r'))) > 0 or len(json.load(output_failure_dir.open('r'))) > 0): return
    if output_common_dir.exists() and len(json.load(output_common_dir.open('r'))) > 0: return
    output_success_dir.parent.mkdir(exist_ok=True)
    output_failure_dir.parent.mkdir(exist_ok=True)
    output_common_dir.parent.mkdir(exist_ok=True)
    tasks = bfs_single_theorem(json_file_path)
    if tasks==[]:return
    tasks_queue = Queue()
    for v in tasks:
        tasks_queue.put(v)
    
    search_pool = SearcherPool()
    for i in range(num_of_mcts):
        search_pool.push(Searcher(model_pool=model_actors))
    all_results = []
    threads = []
    # Submit the task to search_pool and write the result to recordFILE
    def worker():
        while not tasks_queue.empty():
            task = tasks_queue.get()
            # print("task submit:", task)
            results = search_pool.submit(lambda a, v: a.alphazero_search(v), task)
            if results is not None:
                all_results.extend(results)

    for i in range(num_of_actors):
        t = Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    all_results = list(set(all_results))
    tmp_results = []
    for i in all_results:
        tmp_results.extend(get_alltactic(i))
    all_results = list(set(tmp_results))
    all_results = [i.to_json() for i in all_results]

    write_record(all_results, output_common_dir)

if __name__ == "__main__":
    
    # The path of the JSON file extracted by Lean4kit
    file_dir = "./json_data/valid"

    # The path of the folder where the search results are saved
    output_dir="./results"

    # The path of the file where the failed theorem search results are saved
    failed_path = "./failed.txt"
    for entry in os.listdir(file_dir):
        full_path = os.path.join(file_dir, entry)
        if os.path.isfile(full_path) and entry.endswith('.json'):
            with open(full_path, 'r') as file:
                code = file.read()

            print(full_path) 
            try:
                search_single_theorem(full_path, output_dir)
            except Exception as e:
                print(e)
                with open(failed_path, 'a') as failed_file:
                    failed_file.write(f"{full_path}\n") 
                continue
