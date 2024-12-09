from components.commander import CommandExecutor
from components.tools import use_tool, summary_tool_result

if __name__ == "__main__":
    executer = CommandExecutor()
    while True:
        msg = input("请输入指令：")
        print(f"用户输入：{msg}")
        if msg == "exit":
            break
        
        result = executer.generate_cmd(msg)
        if isinstance(result, str):
            # 生成命令行
            print(f"生成命令：{result}")
            status_code, output = executer.execute_cmd(result)
            reply = executer.summary_exe(msg, result, status_code, output)
        elif isinstance(result, dict):
            # function calling
            print(f"function calling: {result}")
            result = use_tool(result)
            reply = summary_tool_result(msg, result)
        else:
            reply = "无"
        print("输出结果：")
        print(reply)
        print("\n")