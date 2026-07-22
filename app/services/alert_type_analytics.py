from collections import Counter
import os


LOG_FILE = os.path.join("logs", "alerts.log")


def get_alert_type_statistics():

    counts = Counter()

    if not os.path.exists(LOG_FILE):
        return {}

    with open(LOG_FILE, "r", encoding="utf-8") as file:

        for line in file:

            if "[WARNING]" not in line and "[CRITICAL]" not in line:
                continue

            if "High CPU Usage" in line:
                counts["High CPU Usage"] += 1

            elif "High RAM Usage" in line:
                counts["High RAM Usage"] += 1

            elif "High Disk Usage" in line:
                counts["High Disk Usage"] += 1

            elif "Suspicious File Activity" in line:
                counts["Suspicious File Activity"] += 1

            else:
                counts["Other"] += 1

    return dict(counts)