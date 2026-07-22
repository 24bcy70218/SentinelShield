import os
from datetime import datetime

ALERT_LOG = "logs/alerts.log"


def create_alert(level, title, message):

    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alert = f"[{timestamp}] [{level}] {title} - {message}"

    print(alert)

    with open(ALERT_LOG, "a", encoding="utf-8") as file:
        file.write(alert + "\n")