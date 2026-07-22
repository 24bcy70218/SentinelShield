from datetime import datetime, timedelta
from app.services.alert_service import create_alert

# Store the last time each alert was generated
last_alert_time = {}

# Cooldown period
COOLDOWN = timedelta(seconds=60)


def can_send_alert(alert_key):
    now = datetime.now()

    if alert_key not in last_alert_time:
        last_alert_time[alert_key] = now
        return True

    if now - last_alert_time[alert_key] >= COOLDOWN:
        last_alert_time[alert_key] = now
        return True

    return False


def check_system_alerts(system):

    cpu = system["cpu"]
    ram = system["memory"]
    disk = system["disk"]

    # CPU Alerts
    if cpu >= 90 and can_send_alert("cpu_critical"):
        create_alert(
            "CRITICAL",
            "High CPU Usage",
            f"CPU usage reached {cpu}%"
        )

    elif cpu >= 80 and can_send_alert("cpu_warning"):
        create_alert(
            "WARNING",
            "High CPU Usage",
            f"CPU usage reached {cpu}%"
        )

    # RAM Alerts
    if ram >= 90 and can_send_alert("ram_critical"):
        create_alert(
            "CRITICAL",
            "High RAM Usage",
            f"RAM usage reached {ram}%"
        )

    elif ram >= 80 and can_send_alert("ram_warning"):
        create_alert(
            "WARNING",
            "High RAM Usage",
            f"RAM usage reached {ram}%"
        )

    # Disk Alerts
    if disk >= 95 and can_send_alert("disk_critical"):
        create_alert(
            "CRITICAL",
            "Disk Almost Full",
            f"Disk usage reached {disk}%"
        )