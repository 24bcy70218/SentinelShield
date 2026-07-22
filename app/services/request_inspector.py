from flask import request
from datetime import datetime
import os

# Log file path
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "requests.log")


def inspect_request():
    """
    Collect information about every incoming HTTP request.
    """

    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": request.remote_addr,
        "method": request.method,
        "path": request.path,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "query": request.args.to_dict(),
        "form": request.form.to_dict()
    }

    return data


def log_request(request_info):
    """
    Save every request to requests.log
    """

    os.makedirs(LOG_DIR, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write("=" * 60 + "\n")

        file.write(f"Time: {request_info['time']}\n")
        file.write(f"IP: {request_info['ip']}\n")
        file.write(f"Method: {request_info['method']}\n")
        file.write(f"Path: {request_info['path']}\n")
        file.write(f"User-Agent: {request_info['user_agent']}\n")
        file.write(f"Query: {request_info['query']}\n")
        file.write(f"Form: {request_info['form']}\n")

        file.write("=" * 60 + "\n\n")