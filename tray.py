from flask import Flask, request, jsonify, send_from_directory
from components.commander import CommandExecutor
from components.tools import use_tool, summary_tool_result, check_if_tool
from utils.logger import loginfo

import threading
import webbrowser
import pystray
from PIL import Image, ImageDraw

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

# Function to create an image for the tray icon
def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill='black')
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill='black')
    return image

# Function to start the Flask app
def run_flask():
    app.run(port=5000)

# Function to handle tray icon click
def on_clicked(icon, item):
    if item.text == "Open":
        webbrowser.open("http://127.0.0.1:5000")
    elif item.text == "Quit":
        icon.stop()
        # Stop the Flask server
        func = request.environ.get('werkzeug.server.shutdown')
        if func:
            func()

# Create and run the tray icon
def run_tray():
    icon = pystray.Icon("FlaskApp")
    icon.icon = create_image()
    icon.menu = pystray.Menu(
        pystray.MenuItem("Open", on_clicked),
        pystray.MenuItem("Quit", on_clicked)
    )
    icon.run()

# Run Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Run the tray icon
run_tray()