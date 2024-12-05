from components.commander import CommandExecutor
from components.path import find_install_path


if __name__ == "__main__":
    executer = CommandExecutor()
    while True:
        msg = input("请输入指令：")
        print(f"用户输入：{msg}")
        if msg == "exit":
            break

        reply = executer.process_message(msg)
        print("输出结果：")
        print(reply)
        print("\n")