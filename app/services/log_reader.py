import os

LOG_FILE = "logs/file_events.log"


def get_recent_events(limit=10):
    """
    Return the latest log entries.
    """

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines if line.strip()]

    return lines[-limit:][::-1]