import psutil
import platform
from datetime import datetime


def get_system_info():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory().percent

    disk = psutil.disk_usage("/").percent

    processes = len(psutil.pids())

    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    net = psutil.net_io_counters()

    return {
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "processes": processes,

        "hostname": platform.node(),
        "system": platform.system(),
        "release": platform.release(),

        "uptime": str(uptime).split(".")[0],

        "upload": round(net.bytes_sent / (1024 * 1024), 2),
        "download": round(net.bytes_recv / (1024 * 1024), 2)
    }


def get_running_processes(limit=15):

    process_list = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):

        try:

            process_list.append({

                "pid": proc.info["pid"],

                "name": proc.info["name"],

                "cpu": proc.info["cpu_percent"],

                "memory": round(proc.info["memory_percent"], 2)

            })

        except:

            pass

    process_list = sorted(
        process_list,
        key=lambda x: x["cpu"],
        reverse=True
    )

    return process_list[:limit]