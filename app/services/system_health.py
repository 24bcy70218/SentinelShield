from app.services.alert_reader import get_recent_alerts


def calculate_health_score():

    alerts = get_recent_alerts(20)   # Only recent alerts

    critical = 0
    warning = 0
    info = 0

    for alert in alerts:

        level = alert.get("level", "").lower()

        if level == "critical":
            critical += 1
        elif level == "warning":
            warning += 1
        else:
            info += 1

    score = 100

    score -= critical * 10
    score -= warning * 3
    score -= info * 1

    score = max(0, min(100, score))

    if score >= 90:
        status = "Excellent"
        color = "success"

    elif score >= 75:
        status = "Good"
        color = "primary"

    elif score >= 50:
        status = "Warning"
        color = "warning"

    else:
        status = "Critical"
        color = "danger"

    return {
        "score": score,
        "status": status,
        "color": color,
        "critical": critical,
        "warning": warning,
        "info": info
    }