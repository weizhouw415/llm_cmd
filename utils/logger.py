import datetime

def loginfo(message: str):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[INFO] {timestamp} - {message}")

def logerror(message: str):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[ERROR] {timestamp} - {message}")