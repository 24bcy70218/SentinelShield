from collections import defaultdict
import os


def get_alert_timeline():

    logfile = os.path.join("logs", "alerts.log")

    if not os.path.exists(logfile):
        return []

    timeline = defaultdict(int)

    with open(logfile, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:
                # Extract:
                # [2026-07-19 04:57:26]
                timestamp = line.split("]")[0].replace("[", "")

                # Keep only YYYY-MM-DD HH:MM
                minute = timestamp[:16]

                timeline[minute] += 1

            except Exception:
                continue

    result = []

    for minute in sorted(timeline.keys()):
        result.append({
            "time": minute,
            "count": timeline[minute]
        })

    return result