import subprocess, json
from utils.llm import qwen_vllm_invoke as qwen_invoke
from utils.llm import qianfan_invoke
from utils.logger import loginfo, logerror
from utils.prompt import (
    PROMPT_GENERATE_CMD, 
    PROMPT_SUMMARY_EXECUTION
)

class CommandExecutor:
    def generate_cmd(self, msg: str) -> str:
        # result = qwen_invoke(msg, system=PROMPT_GENERATE_CMD)
        result = qianfan_invoke(
            msg, 
            system=PROMPT_GENERATE_CMD
        )
        loginfo(f"generate cmd: {result}")
        if isinstance(result, str):
            result = result.replace("`", "").replace("```", "").strip()
            loginfo(f"stripped cmd: {result}")
        return result

    def execute_cmd(self, cmd: str) -> tuple[int, str]:
        try:
            if cmd.startswith("powershell"):
                cmd = cmd.replace("powershell -command", "").replace("powershell", "").strip()
                loginfo(f"Stripped powershell cmd: {cmd}")
                process = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                if cmd.startswith("systeminfo"):
                    cmd = cmd.split("|")[0].strip()
                    loginfo(f"Stripped cmd: {cmd}")
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            stdout, stderr = process.communicate()
            code = int(process.returncode)
            result = stdout.decode(errors='ignore') if stdout else ""
            error = stderr.decode(errors='ignore') if stderr else ""
            loginfo(f"code: {code}")
            if code == 0:
                loginfo(f"执行结果: {result}")
                return process.returncode, result
            else:
                logerror(f"执行错误: {error}")
                return process.returncode, error
        except Exception as e:
            logerror(f"execute_cmd error: {e}")
            return -1, str(e)
    
    def summary_exe(self, msg: str, cmd: str, status: int, result: str = "") -> str:
        try:
            prompt = PROMPT_SUMMARY_EXECUTION.format(
                msg=msg,
                cmd=cmd,
                code=status,
                result=result
            )
            reply = qianfan_invoke(prompt)
            return reply
        except Exception as e:
            logerror(f"summary_exe error: {e}")
            return e