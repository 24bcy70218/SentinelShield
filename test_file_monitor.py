import time
from watchdog.observers import Observer
from app.services.file_monitor import FileMonitor

WATCH_FOLDER = "watch_folder"

observer = Observer()
observer.schedule(FileMonitor(), WATCH_FOLDER, recursive=True)

observer.start()

print("=" * 50)
print(" SentinelShield File Monitor Started ")
print("=" * 50)
print(f"Monitoring: {WATCH_FOLDER}")
print("Press Ctrl+C to stop.")
print("=" * 50)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()