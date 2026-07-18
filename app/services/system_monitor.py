import psutil


def get_system_info():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory().percent

    disk = psutil.disk_usage("/").percent

    processes = len(psutil.pids())

    return {
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "processes": processes
    }