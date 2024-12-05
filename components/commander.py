import subprocess
from utils.llm import qwen_vllm_invoke as qwen_invoke
from utils.llm import qianfan_invoke
from utils.logger import loginfo, logerror
from utils.prompt import (
    PROMPT_CHECK_IF_CMD,
    PROMPT_CHECK_CMD_PROBLEM,
    PROMPT_GENERATE_CMD, 
    PROMPT_SUMMARY_EXECUTION
)

class CommandExecutor:
    def check_win_prob(self, msg: str) -> bool:
        final_prompt = PROMPT_CHECK_CMD_PROBLEM.format(input=msg)
        result = qwen_invoke(final_prompt)
        loginfo(f"是否为cmd场景：{result}")
        if result == 'Y' or result.startswith('Y'):
            return True
        return False
    
    def check_win_cmd(self, cmd: str) -> bool:
        final_prompt = PROMPT_CHECK_IF_CMD.format(cmd=cmd)
        result = qwen_invoke(final_prompt)
        loginfo(f"是否为命令行：{result}")
        if result == 'Y' or result.startswith('Y'):
            return True
        return False

    def generate_cmd(self, msg: str) -> str:
        # result = qwen_invoke(msg, system=PROMPT_GENERATE_CMD)
        result = qianfan_invoke(msg, system=PROMPT_GENERATE_CMD)
        loginfo(f"generate cmd: {result}")
        result = result.strip("`").strip("```").strip()
        loginfo(f"stripped cmd: {result}")
        return result

    def execute_cmd(self, cmd: str) -> tuple[int, str]:
        try:
            if cmd.startswith("powershell"):
                cmd = cmd.replace("powershell", "").strip()
                loginfo(f"Stripped powershell cmd: {cmd}")
                process = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            stdout, stderr = process.communicate()
            if stdout == 0:
                return process.returncode, stdout.decode()
            else:
                return process.returncode, stderr.decode()
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
    
    def process_message(self, msg: str) -> str:
        cmd = self.generate_cmd(msg)
        status_code, output = self.execute_cmd(cmd)
        reply = self.summary_exe(msg, cmd, status_code, output)
        return reply

if __name__ == "__main__":
    executer = CommandExecutor()
    
    # msg = "查看内存使用情况"
    # msg = "请帮我创建一个2.txt的文件在当前文件夹"
    # msg = "查看当前文件夹下的所有文件"
    # msg = "查看我的内存使用情况"
    msg = "查看我的cpu使用率"
    print(f"用户输入：{msg}")

    reply = executer.process_message(msg)
    print("输出结果：")
    print(reply)
    print("\n")