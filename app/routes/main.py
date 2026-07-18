from flask import jsonify
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.system_monitor import get_system_info
from app.services.log_reader import get_recent_events

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():

    system = get_system_info()

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