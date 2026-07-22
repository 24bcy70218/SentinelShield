from watchdog.events import FileSystemEventHandler
from collections import deque
from datetime import datetime
from app.services.alert_service import create_alert
import os

LOG_FILE = "logs/file_events.log"

# Store timestamps of recent file events
recent_events = deque()

# Prevent duplicate alerts
last_burst_alert = None

# Configuration
BURST_LIMIT = 10       # Trigger alert after 10 events
BURST_WINDOW = 30      # Within 30 seconds
COOLDOWN = 60          # Wait 60 seconds before sending same alert again


def detect_file_burst():
    global last_burst_alert

    now = datetime.now()

    # Add current event timestamp
    recent_events.append(now)

    # Remove timestamps older than BURST_WINDOW
    while recent_events and (now - recent_events[0]).total_seconds() > BURST_WINDOW:
        recent_events.popleft()

    # Check if event burst detected
    if len(recent_events) >= BURST_LIMIT:

        # Cooldown check
        if (
            last_burst_alert is None or
            (now - last_burst_alert).total_seconds() >= COOLDOWN
        ):

            create_alert(
                "CRITICAL",
                "Suspicious File Activity",
                f"{len(recent_events)} file events detected within {BURST_WINDOW} seconds"
            )

            last_burst_alert = now


class FileMonitor(FileSystemEventHandler):

    def log_event(self, event_type, message):

        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log = f"[{timestamp}] {event_type:<10} {message}"

        print(log)

        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log + "\n")

    def on_created(self, event):
        if not event.is_directory:
            self.log_event("CREATED", event.src_path)
            detect_file_burst()

    def on_modified(self, event):
        if not event.is_directory:
            self.log_event("MODIFIED", event.src_path)
            detect_file_burst()

    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event("DELETED", event.src_path)
            detect_file_burst()

    def on_moved(self, event):
        if not event.is_directory:
            self.log_event(
                "MOVED",
                f"{event.src_path} -> {event.dest_path}"
            )
            detect_file_burst()

def get_file_events(limit=100):

    events = []

    if not os.path.exists(LOG_FILE):
        return events

    with open(LOG_FILE, "r", encoding="utf-8") as file:

        lines = file.readlines()[-limit:]

    for line in reversed(lines):

        try:

            timestamp = line[1:20]

            rest = line[22:].strip()

            parts = rest.split(maxsplit=1)

            event = parts[0]

            path = parts[1] if len(parts) > 1 else ""

            events.append({

                "time": timestamp,

                "event": event,

                "path": path

            })

        except:
            pass

    return events

