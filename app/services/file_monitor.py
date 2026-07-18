from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os

LOG_FILE = "logs/file_events.log"


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

    def on_modified(self, event):
        if not event.is_directory:
            self.log_event("MODIFIED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event("DELETED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.log_event(
                "MOVED",
                f"{event.src_path} -> {event.dest_path}"
            )