from app.services.system_health import calculate_health_score


def get_threat_level():

    health = calculate_health_score()

    score = health["score"]

    if score >= 90:
        return {
            "level": "LOW RISK",
            "message": "System operating normally.",
            "color": "success",
            "icon": "🟢"
        }

    elif score >= 75:
        return {
            "level": "GUARDED",
            "message": "Minor security concerns detected.",
            "color": "primary",
            "icon": "🔵"
        }

    elif score >= 50:
        return {
            "level": "ELEVATED",
            "message": "Increased monitoring recommended.",
            "color": "warning",
            "icon": "🟡"
        }

    else:
        return {
            "level": "CRITICAL",
            "message": "Immediate attention required.",
            "color": "danger",
            "icon": "🔴"
        }