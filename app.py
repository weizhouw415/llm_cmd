from flask import Flask, request, jsonify, send_from_directory
from components.commander import CommandExecutor
from components.tools import use_tool, summary_tool_result, check_if_tool
from utils.logger import loginfo

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.get_json()
    msg = data.get('query', '')
    try:
        if check_if_tool(msg):
            result = use_tool(msg)
            reply = summary_tool_result(msg, result)
        else:
            # 生成命令行
            executer = CommandExecutor()
            result = executer.generate_cmd(msg)
            status_code, output = executer.execute_cmd(result)
            reply = executer.summary_exe(msg, result, status_code, output)
        loginfo(f"Final reply: {reply}")
        resp = {"Code": 0, "reply": reply}
        return jsonify(resp)
    except Exception as e:
        resp = {"Code": -1, "reply": str(e)}
        return jsonify(resp)

if __name__ == "__main__":
    app.run(port=7000, debug=True)