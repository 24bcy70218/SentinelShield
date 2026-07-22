import os
import re

ALERT_LOG = "logs/alerts.log"


def get_alert_count():
    if not os.path.exists(ALERT_LOG):
        return 0

    with open(ALERT_LOG, "r", encoding="utf-8") as file:
        return len(file.readlines())


def get_recent_alerts(limit=10):

    if not os.path.exists(ALERT_LOG):
        return []

    with open(ALERT_LOG, "r", encoding="utf-8") as file:
        lines = file.readlines()

    alerts = []

    pattern = r"\[(.*?)\] \[(.*?)\] (.*?) - (.*)"

    for line in reversed(lines[-limit:]):

        match = re.match(pattern, line.strip())

        if match:

            alerts.append({
                "time": match.group(1),
                "level": match.group(2),
                "title": match.group(3),
                "message": match.group(4)
            })

    return alerts