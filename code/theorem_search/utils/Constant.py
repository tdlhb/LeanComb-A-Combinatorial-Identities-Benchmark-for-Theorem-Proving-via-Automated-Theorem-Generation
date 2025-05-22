from loguru import logger
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0" 
import torch
import vllm
from tqdm import *
from utils.lean4Kit.Lean4Kit import *
logger.remove()
logger.add("../logs/{time}.log")
'''Global logger'''
PATH_PREFIX = ""




NUM_CPUS = 3
'''Number of CPU processes used'''


GPU_AVAILABLE_COUNT = 1 # torch.cuda.device_count() 
'''Number of available GPUs'''


MODEL_ACTOR_GPU_USAGE = 0.9
'''The proportion of video memory occupied by each model actor needs to be slightly larger than that in vllm config'''

MODLE_PATH = ""
VLLM_CONFIG = {
    "model": MODLE_PATH, 
    "max_model_len": 4096, 
    "gpu_memory_utilization": 0.85, 
    "swap_space": 4.0, 
    "trust_remote_code": True, 
    "tensor_parallel_size": 1,
    "dtype": "bfloat16", 
}
'''Parameters when VLLM loads models'''


SAMPLE_CONFIG = {
    "n": 16, 
    "temperature": 0.7, 
    "max_tokens": 2048,
    "logprobs": 0,
}
'''Sampling parameters during VLLM inference'''



PROMPT_CONFIG = {
    "system": "You are using Lean4 for theorem proving", 
    "instruction": "", 
    "input": "",
    "prompt_template": 
        f'''You are proving a theorem in Lean 4.\nBased on the current state of the theorem, provide the most reasonable proof tactic.\nEnsure that the tactic you provide is syntactically correct according to Lean 4's tactic syntax and is effective in progressing the proof.\n\n
    [Current State]: $ts\n[Output Tactic]: \n'''
}
'''prompt'''


DEEPSEEK_PROMPT_CONFIG = {
    "system": "", 
    "instruction": "", 
    "input": "",
    "prompt_template":
        f'''Complete the following Lean 4 code:

```lean4
$ts'''
}

DEEPSEEK_PASSK = 32

DEEPSEEK_SAMPLE_CONFIG = {
    "n": 1, 
    "temperature": 0.95, 
    "max_tokens": 2048,
    "logprobs": 0,
}


MODEL_LOAD_GAP = 30
'''The time interval between loading two adjacent models in the model thread pool'''




REPL_VERSION = "4.14"
'''The version of Lean4'''


LEAN_WORKDIR = "./mathlib4"
'''Root directory of Lean project'''

TACRIC_NUMBER = 16
VERBOSE = True
TIME_OUT = 300
SEARCH_TIME_BUDGET = 3000
EXPAND_NUMBER = 1000
USE_RL = True

POLICY_MODEL_PATH = "models/policy_model"
VALUE_MODEL_PATH = "models/value_model"
