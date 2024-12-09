import streamlit as st
from components.commander import CommandExecutor
from components.tools import use_tool, summary_tool_result

# 初始化 CommandExecutor
executer = CommandExecutor()

# Streamlit 页面标题
st.title("问答系统")

# 用户输入
msg = st.text_input("请输入指令：")

if st.button("提交"):
    st.write(f"用户输入：{msg}")
    if msg == "exit":
        st.write("程序已退出")
    else:
        result = executer.generate_cmd(msg)
        if isinstance(result, str):
            # 生成命令行
            st.write(f"生成命令：{result}")
            status_code, output = executer.execute_cmd(result)
            reply = executer.summary_exe(msg, result, status_code, output)
        elif isinstance(result, dict):
            # function calling
            st.write(f"function calling: {result}")
            result = use_tool(result)
            reply = summary_tool_result(msg, result)
        else:
            reply = "无"
        st.write("输出结果：")
        st.write(reply)