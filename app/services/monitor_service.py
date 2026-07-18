import threading

from watchdog.observers import Observer

from app.services.file_monitor import FileMonitor


observer = None


def start_file_monitor():

    global observer

    if observer is not None:
        return

    observer = Observer()

    observer.schedule(
        FileMonitor(),
        "watch_folder",
        recursive=True
    )

    observer.start()

    print("🛡 File Integrity Monitor Started")


def start_monitor_thread():

    thread = threading.Thread(
        target=start_file_monitor,
        daemon=True
    )

    thread.start()