from datetime import datetime

def debug(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time + " " + msg)