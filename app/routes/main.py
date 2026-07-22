from flask import Blueprint, render_template, jsonify, send_file
from flask_login import login_required, current_user
import os

from app.services.system_monitor import get_system_info
from app.services.log_reader import get_recent_events
from app.services.alert_engine import check_system_alerts
from app.services.alert_reader import get_alert_count, get_recent_alerts
from app.services.security_analytics import get_alert_statistics
from app.services.timeline_service import get_alert_timeline
from app.services.system_health import calculate_health_score
from app.services.threat_level import get_threat_level
from app.services.alert_type_analytics import get_alert_type_statistics
from flask import jsonify
from app.services.system_monitor import get_system_info
from app.services.system_monitor import get_system_info, get_running_processes
from app.services.file_monitor import get_file_events
from app.services.csv_export import export_alerts_to_csv
from flask import send_file
from app.services.report_service import generate_report as generate_pdf_report
from app.services.network_monitor import (
    get_network_status,
    get_connections
)

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():

    system = get_system_info()

    check_system_alerts(system)

    return render_template(
        "dashboard.html",
        user=current_user,
        system=system
    )


@main.route("/system-info")
@login_required
def system_info():

    system = get_system_info()

    return jsonify(system)


@main.route("/recent-events")
@login_required
def recent_events():

    events = get_recent_events()

    return jsonify(events)


@main.route("/alert-count")
@login_required
def alert_count():

    return {
        "count": get_alert_count()
    }


@main.route("/recent-alerts")
@login_required
def recent_alerts():

    return jsonify(get_recent_alerts())


@main.route("/latest-alert")
@login_required
def latest_alert():

    alerts = get_recent_alerts(1)

    if alerts:
        return jsonify(alerts[0])

    return jsonify({})


@main.route("/generate-report")
@login_required
def generate_report():

    report_path = generate_pdf_report()

    return send_file(report_path, as_attachment=True)

@main.route("/alert-stats")
@login_required
def alert_stats():

    return jsonify(
        get_alert_statistics()
    )


@main.route("/alert-timeline")
@login_required
def alert_timeline():

    return jsonify(
        get_alert_timeline()
    )

@main.route("/health-score")
@login_required
def health_score():

    return jsonify(
        calculate_health_score()
    )

@main.route("/threat-level")
@login_required
def threat_level():

    return jsonify(
        get_threat_level()
    )

@main.route("/alert-types")
@login_required
def alert_types():

    return jsonify(
        get_alert_type_statistics()
    )

from flask import send_file
import os

@main.route("/export-alerts")
@login_required
def export_alerts():

    csv_path = export_alerts_to_csv()

    return send_file(
        os.path.abspath(csv_path),
        as_attachment=True,
        download_name="alerts.csv"
    )


@main.route("/attack-intelligence")
@login_required
def attack_intelligence():

    return render_template("ip_dashboard.html")



@main.route("/monitoring")
@login_required
def monitoring():

    system = get_system_info()

    return render_template(
        "monitoring.html",
        system=system
    )


@main.route("/api/system-status")
@login_required
def api_system_status():

    return jsonify(get_system_info())


@main.route("/api/processes")
@login_required
def api_processes():

    return jsonify(get_running_processes())

@main.route("/files")
@login_required
def files():
    return render_template("files.html")


@main.route("/api/file-events")
@login_required
def api_file_events():
    return jsonify(get_file_events())

@main.route("/network")
@login_required
def network():
    return render_template("network.html")

@main.route("/api/network-status")
@login_required
def api_network_status():
    return jsonify(get_network_status())

@main.route("/api/network-connections")
@login_required
def api_network_connections():
    return jsonify(get_connections())

