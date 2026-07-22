from app.services.alert_reader import get_recent_alerts


def get_alert_statistics():

    alerts = get_recent_alerts(1000)

    stats = {
        "critical": 0,
        "warning": 0,
        "info": 0
    }

    for alert in alerts:

        level = alert.get("level", "").lower()

        if level in stats:
            stats[level] += 1

    stats["total"] = (
        stats["critical"]
        + stats["warning"]
        + stats["info"]
    )

    return stats