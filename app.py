from flask import Flask, request, jsonify, send_from_directory
from components.commander import CommandExecutor
from components.tools import use_tool, summary_tool_result

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.get_json()
    msg = data.get('query', '')
    
    executer = CommandExecutor()
    try:
        result = executer.generate_cmd(msg)
        if isinstance(result, str):
            # 生成命令行
            status_code, output = executer.execute_cmd(result)
            reply = executer.summary_exe(msg, result, status_code, output)
        elif isinstance(result, dict):
            # function calling
            result = use_tool(result)
            reply = summary_tool_result(msg, result)
        else:
            reply = "无"
        resp = {"Code": 0, "reply": reply}
        return jsonify(resp)
    except Exception as e:
        resp = {"Code": -1, "reply": str(e)}
        return jsonify(resp)

if __name__ == "__main__":
    app.run(port=7000, debug=True)