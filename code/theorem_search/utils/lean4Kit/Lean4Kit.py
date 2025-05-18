import subprocess
import json
import signal
from pathlib import Path
import sys
from .LeanKitException import *
import time
class TacticState():
    def __init__(self, res, state_type="cmd"):
        self.finishFlag = False
        self.proofStates = []
        self.goals = []
        self.error = False
        self.messages = res.get('messages')
        if self.messages == None:self.messages = res.get("message")
        self.sorries = res.get("sorries")
        self.env = res.get("env")
        if self.messages:
            if isinstance(self.messages,str):
                if self.messages.find("error")!=-1:
                    self.error = True
            else:
                for i in self.messages:
                    if i["severity"].find('error')!=-1 and not i['data'].startswith("unsolved goals"):
                        self.error = True
        else:
            if not self.sorries:
                self.error = False
                self.finishFlag = True
        if state_type == 'tactic':
            self.init_tacticState(res)
        elif state_type == 'have':
            self.init_haveTacticState(res)
        else:
            self.init_cmdState(res)

    def getTacticState(self) -> str:
        """Obtain the current proof status"""
        if len(self.goals)==0:
            return "no goals"
        goal = self.goals[0]
        if isinstance(goal,list):
            if len(goal):
                goal_ = ""
                for i in goal:
                    goal_ += i
                return goal_
            else: return "no goals"
        else:
            return goal
    def init_haveTacticState(self, res):
        self.init_cmdState(res)
        self.proofStates.append((res.get('proofState')))
        self.goals.append(res.get("goals"))
    def init_cmdState(self, res):
        if self.sorries and self.sorries != []:
            self.finishFlag = False
            self.proofStates.append(self.sorries[-1]["proofState"])
            self.goals.append(self.sorries[-1]["goal"])

    def init_tacticState(self, res):
        self.proofStates.append((res.get('proofState')))
        self.goals.append(res.get("goals"))

        if self.goals[0] == None:
            self.error = True
        if not self.error and len(self.goals[0]) == 0:
            self.finishFlag = True
        else:
            self.finishFlag = False

    def isFinish(self):
        return self.finishFlag

    def isError(self):
        return self.error

    def print(self):
        if self.proofStates:
            print("proofStates:", self.proofStates)
        if self.goals:
            print("goals:", self.goals)
        print("error:", self.error)
        print("messages:", self.messages)
        print("sorries:", self.sorries) 
        print("is finish:", self.finishFlag)
        print()

class Lean4Kit:
    def __init__(self, work_dir, repl_version, verbose=False):
        repl_path = Path(__file__).parent.resolve() / f'repl_v{repl_version}'
        if verbose:
            print("repl_path:", repl_path)

        cmd = f"lake env {repl_path}"

        try:
            self.proc = subprocess.Popen(
                cmd,
                cwd=work_dir,
                shell=True,  
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True 
            )

            if verbose:
                print(f"Process started，PID: {self.proc.pid}")

        except Exception as e:
            raise RuntimeError(f"Process startup failed: {e}")

    def run_import(self, code, env=None, verbose=False):
        if env != None:
            command = json.dumps({
                "cmd": code,
                "env": env
            })
        else:
            command = json.dumps({
                "cmd": code
            })
        return self.__runCommand__(command, verbose=verbose)

    def new_thm(self, code, env=None, verbose=False):
        if env != None:
            command = json.dumps({
                "cmd": code+" := by sorry",
                "env": env
            })
        else:
            command = json.dumps({
                "cmd": code+" := by sorry"
            })
        try:
            result = self.__runCommand__(command, verbose=verbose)
        except TypeError:
            raise TheoremInitException("Theorem environment error or theorem description error")
        return result
    def run_tactic(self, tactic, proofState, cmd_type='tactic', verbose=False):
        command = json.dumps({
                "tactic": tactic,
                "proofState": proofState
            })
        return self.__runCommand__(command, cmd_type, verbose)
    def run_have_tactic(self, tactic, proofState, cmd_type='have', verbose=False):
        command = json.dumps({
                "tactic": tactic+":= by sorry",
                "proofState": proofState
            })
        return self.__runCommand__(command, cmd_type, verbose)
    def is_correct_and_finished(self, code, verbose=False,timeout=160):
        """
        Complete code validation for correctness
        """
        command = json.dumps({
            "cmd": code
        })
        try:
            stat = self.__runCommand__(command, verbose=verbose,timeout=timeout)
        except:
            print("Error during verification")
            raise VerificationFailedException("Error verifying the correctness of the theorem")
        messages = stat.messages
        sorries = stat.sorries
        # stat.print()
        if sorries and len(sorries): return False
        if messages:
            if isinstance(messages,str):
                if messages.find("error")!=-1:
                    return False
            else:
                for i in messages:
                    if i["severity"]=="warning" and i["data"].find("sorry")!=-1:
                        return False 
                    elif i["severity"]=="error":
                        return False 
        return True
    def run_allTactics(self, code, env=None, verbose=True):

        if env:
            command = json.dumps({
                "cmd": code,
                "infotree": "substantive"
            })
        else:
            command = json.dumps({
                "cmd": code,
                "infotree": "substantive"
            })

        try:
            self.proc.stdin.write(command + "\n")
            self.proc.stdin.flush()

            response = ""
            self.proc.stdin.write("\n")
            self.proc.stdin.flush()
            while True:
                line = self.proc.stdout.readline()
                if not line:
                    break
                response += line
                try:
                    json_data = json.loads(response)
                    if verbose:
                        print("JSON parsing successful:", json.dumps(json_data, indent=2))
                    return json_data
                except json.JSONDecodeError:
                    if verbose:
                        print("Failed to parse JSON, trying again")
                    continue

        except Exception as e:
            raise RuntimeError(f"Command execution failed: {e}")


    def __send_command(self, command, timeout=60):
        """Send commands to child processes and obtain output, and set timeout time"""
        if self.proc.stdin is None or self.proc.stdout is None:
            raise RuntimeError("Child process I/O unavailable")

        try:
            self.proc.stdin.write(command + "\n")
            self.proc.stdin.flush()

            response = ""
            self.proc.stdin.write("\n")
            self.proc.stdin.flush()

            start_time = time.time()

            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    raise TimeoutError(f"Command execution timeout（{timeout}s）")

                line = self.proc.stdout.readline()
                if not line:  
                    break
                response += line
                try:
                    json_data = json.loads(response)
                    return json_data
                except json.JSONDecodeError:
                    continue
        except TimeoutError as te:
            raise TimeoutError(f"command timeout：{te}")
        except Exception as e:
            raise RuntimeError(f"Command execution failed: {e}")

    def __runCommand__(self, command, cmd_type="cmd", verbose=False,timeout=60):
        """Run the command and return TacticState"""
        if verbose:
            print(f"Processing command: {command}")
        try:
            json_response = self.__send_command(command,timeout=timeout)
            return TacticState(json_response, cmd_type)
        except json.JSONDecodeError as e:
            raise InteractiveEOFException(f"Failed to parse JSON: {e}")
        except Exception as e:
            print(e)
            raise RuntimeError(f"Command execution failed: {e}")
    def close(self):
        if self.proc:
            self.proc.terminate()
            self.proc.wait()
