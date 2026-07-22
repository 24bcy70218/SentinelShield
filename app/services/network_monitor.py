import psutil
import time

last_sent = psutil.net_io_counters().bytes_sent
last_recv = psutil.net_io_counters().bytes_recv
last_time = time.time()

def get_network_speed():

    global last_sent
    global last_recv
    global last_time

    current = psutil.net_io_counters()

    now = time.time()

    elapsed = now - last_time

    if elapsed <= 0:
        elapsed = 1

    upload = (current.bytes_sent - last_sent) / elapsed
    download = (current.bytes_recv - last_recv) / elapsed

    last_sent = current.bytes_sent
    last_recv = current.bytes_recv
    last_time = now

    return upload, download

def get_network_status():

    io = psutil.net_io_counters()
    upload_speed, download_speed = get_network_speed()

    listening_ports = len([
        conn for conn in psutil.net_connections(kind="inet")
        if conn.status == psutil.CONN_LISTEN
    ])

    established = len([
        conn for conn in psutil.net_connections(kind="inet")
        if conn.status == psutil.CONN_ESTABLISHED
    ])

    return {

        "bytes_sent": round(io.bytes_sent / (1024 * 1024), 2),

        "bytes_recv": round(io.bytes_recv / (1024 * 1024), 2),

        "upload_speed": round(upload_speed / 1024, 2),

        "download_speed": round(download_speed / 1024, 2),

        "packets_sent": io.packets_sent,

        "packets_recv": io.packets_recv,

        "listening_ports": listening_ports,

        "active_connections": established

    }


def get_connections(limit=100):

    connections = []

    for conn in psutil.net_connections(kind="inet"):

        try:

            pid = conn.pid if conn.pid else "-"

            process = "-"

            if conn.pid:

                try:
                    process = psutil.Process(conn.pid).name()
                except:
                    process = "Unknown"

            local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "-"

            remote = (
                f"{conn.raddr.ip}:{conn.raddr.port}"
                if conn.raddr else "-"
            )

            connections.append({

                "pid": pid,

                "process": process,

                "local": local,

                "remote": remote,

                "status": conn.status

            })

        except:
            pass

    return connections[:limit]