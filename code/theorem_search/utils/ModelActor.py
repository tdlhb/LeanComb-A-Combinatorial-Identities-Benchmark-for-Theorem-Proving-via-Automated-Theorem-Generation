from utils.Constant import *
import ray
import ray.util.multiprocessing
import vllm
import transformers
from string import Template
from threading import Lock
import copy
class ModelActorPool:
    def __init__(self) -> None:
        self.actors = []
        self.actors_status = []
        self.lock = Lock()

    def push(self, actor):
        self.actors.append(actor)
        self.actors_status.append(True)
    def submit(self, fn, val):
        idx = 0
        while True:
            with self.lock:
                if self.actors_status[idx]:
                    self.actors_status[idx] = False
                    break
                idx = (idx + 1) % len(self.actors)

        objectRef = fn(self.actors[idx], val)
        results = ray.get(objectRef)

        with self.lock:
            self.actors_status[idx] = True

        return results


ray.init(num_cpus=NUM_CPUS)


@ray.remote(num_cpus=1,num_gpus=MODEL_ACTOR_GPU_USAGE)
class ModelActor:
    def __init__(self, vllm_config: dict, prompt_config: dict,
                 sample_config: dict = None) -> None:
        '''
        Initialize an inference model under the VLLM framework,
        The parameter type of vllm_comfig is dict, and the keyword is the same as vllm
        Note: The placeholder in the template in prompt_comfig is $ts
        '''
        self.prompt_config = prompt_config
        self.sample_config = sample_config
        self.model_name_or_path = vllm_config["model"]
        self.model = vllm.LLM(**vllm_config)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_name_or_path,trust_remote_code=True)
        self.idle = True
    def encode_tactic_state(self,tactic_state, feature_size=100):
        encode_tactic_state = self.tokenizer.encode(str(tactic_state))
        if(len(encode_tactic_state)<=feature_size):
            encode_tactic_state += [0]*(feature_size-len(encode_tactic_state))
        else:
            encode_tactic_state = encode_tactic_state[:feature_size]
        return encode_tactic_state

    def get_model_input(self, proof_state: str) -> str:

        self.system = self.prompt_config["system"] if "system" in self.prompt_config.keys(
        ) else "You are a Lean4 Proof Assistant"
        self.prompt_template = self.prompt_config["prompt_template"]
        self.template = Template(self.prompt_template)

        messages = [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.template.safe_substitute(
                ts=proof_state)}
        ]

        input_text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        print(input_text)
        return input_text

    def generate(self, input_text: str, sample_config: dict = None):
        if sample_config is None:
            sample_config = self.sample_config

        # self.idle = False
        params = vllm.SamplingParams(
            stop=self.tokenizer.eos_token,
            **sample_config
        )

        response = self.model.generate(input_text, params, use_tqdm=False)
        # self.idle = True
        return response

    def generate_tactics_scores(self, ts, sample_config: dict = SAMPLE_CONFIG):
        input_text = self.get_model_input(ts)
        response = self.generate(input_text, sample_config)
        tactics_scores = self.handle_response(response)
        return tactics_scores
    def handle_response(self, response):
        texts, scores = [], []
        for output in response[0].outputs:
            if output.text not in texts:
                try:
                    texts.append(output.text)
                    scores.append(output.cumulative_logprob)
                except Exception as e:
                    # with open("error.log", "w") as f:
                    #     f.write(output.text)
                    print('model output format does not conform json data')

        result = sorted(zip(texts, scores), key=lambda x: -x[1])
        return result
    
    def is_idle(self):
        return self.idle