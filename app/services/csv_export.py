import csv
import os
import re

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

LOG_FILE = os.path.join(BASE_DIR, "logs", "alerts.log")

EXPORT_DIR = os.path.join(BASE_DIR, "reports")


def export_alerts_to_csv():

    os.makedirs(EXPORT_DIR, exist_ok=True)

    csv_path = os.path.join(EXPORT_DIR, "alerts.csv")

    with open(LOG_FILE, "r", encoding="utf-8") as logfile, \
         open(csv_path, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Timestamp",
            "Level",
            "Alert Type",
            "Message"
        ])

        pattern = r"\[(.*?)\]\s+\[(.*?)\]\s+(.*?)\s+-\s+(.*)"

        for line in logfile:

            match = re.match(pattern, line.strip())

            if match:

                timestamp, level, alert_type, message = match.groups()

                writer.writerow([
                    timestamp,
                    level,
                    alert_type,
                    message
                ])

    return csv_path