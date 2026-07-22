from app import create_app
from app.services.request_inspector import inspect_request, log_request
from app.services.sql_injection_detector import detect_sql_injection
from app.services.xss_detector import detect_xss
from app.services.command_injection_detector import detect_command_injection
from app.services.directory_traversal_detector import detect_directory_traversal
from app.services.lfi_detector import detect_lfi
from app.services.rfi_detector import detect_rfi    
from app.services.rate_limiter import check_rate_limit
from app.services.ip_tracker import record_attack
from app.services.ip_tracker import get_ip_statistics
from flask import jsonify
from flask import render_template
from app.services.ip_tracker import is_blocked
from flask import Flask, render_template, jsonify, request
from app.services.ip_tracker import unblock_ip                                                                                                                                                                                                                                                                                                                                         
from app.services.alert_service import create_alert 


app = create_app()


@app.before_request
def monitor_request():

    ip = request.remote_addr

    if is_blocked(ip):
        return (
          "<h1>403 Forbidden</h1>"
          "<p>Your IP has been blocked by SentinelShield.</p>",
          403
        )
    """
    Intercepts every HTTP request before Flask processes it.
    """

    # Collect request information
    request_info = inspect_request()

    # Print request details
    print("\n========== HTTP REQUEST ==========")

    for key, value in request_info.items():
        print(f"{key}: {value}")

    print("==================================\n")

    # Save request to logs/requests.log
    log_request(request_info)

    

    # --------------------------------------------------
    # SQL Injection Detection
    # --------------------------------------------------
    if detect_sql_injection(request_info):

        create_alert(
            "CRITICAL",
            "SQL Injection",
            f"IP={request_info['ip']} | "
            f"Path={request_info['path']} | "
            f"Query={request_info['query']} | "
            f"Form={request_info['form']}"
        )
        
        record_attack(
          request_info["ip"],
          "SQL Injection"
        )

        print("\n🚨 SQL INJECTION DETECTED 🚨")
        print(f"IP: {request_info['ip']}")
        print(f"PATH: {request_info['path']}")
        print(f"QUERY: {request_info['query']}")
        print(f"FORM: {request_info['form']}")
        print("=" * 60)

    # --------------------------------------------------
    # Cross Site Scripting (XSS) Detection
    # --------------------------------------------------
    if detect_xss(request_info):

        create_alert(
            "HIGH",
            "Cross Site Scripting (XSS)",
            f"IP={request_info['ip']} | "
            f"Path={request_info['path']} | "
            f"Query={request_info['query']} | "
            f"Form={request_info['form']}"
        )

        record_attack(
           request_info["ip"],
           "XSS"
        )

        print("\n🚨 XSS ATTACK DETECTED 🚨")
        print(f"IP: {request_info['ip']}")
        print(f"PATH: {request_info['path']}")
        print(f"QUERY: {request_info['query']}")
        print(f"FORM: {request_info['form']}")
        print("=" * 60)

    # --------------------------------------------------
    # Command Injection Detection
    # --------------------------------------------------

    if detect_command_injection(request_info):

        create_alert(
            "CRITICAL",
            "Command Injection",
            f"IP={request_info['ip']} | "
            f"Path={request_info['path']} | "
            f"Query={request_info['query']} | "
            f"Form={request_info['form']}"
        )

        record_attack(
          request_info["ip"],
          "Command Injection"
        )

        print("\n🚨 COMMAND INJECTION DETECTED 🚨")

        print(f"IP: {request_info['ip']}")
        print(f"PATH: {request_info['path']}")
        print(f"QUERY: {request_info['query']}")
        print(f"FORM: {request_info['form']}")

        print("=" * 60)  

    # --------------------------------------------------
    # Directory Traversal Detection
    # --------------------------------------------------

    if detect_directory_traversal(request_info):

       create_alert(
            "CRITICAL",
            "Directory Traversal",
            f"IP={request_info['ip']} | "
            f"Path={request_info['path']} | "
            f"Query={request_info['query']} | "
            f"Form={request_info['form']}"
       )

       record_attack(
          request_info["ip"],
          "Directory Traversal"
       )

       print("\n🚨 DIRECTORY TRAVERSAL DETECTED 🚨")

       print(f"IP: {request_info['ip']}")
       print(f"PATH: {request_info['path']}")
       print(f"QUERY: {request_info['query']}")
       print(f"FORM: {request_info['form']}")

       print("=" * 60)   
    # --------------------------------------------------
    # Local File Inclusion (LFI)
    # --------------------------------------------------

    if detect_lfi(request_info):

        create_alert(
         "CRITICAL",
         "Local File Inclusion (LFI)",
         f"IP={request_info['ip']} | "
         f"Path={request_info['path']} | "
         f"Query={request_info['query']} | "
         f"Form={request_info['form']}"
        )
         
        record_attack(
          request_info["ip"],
          "Local File Inclusion"
        )  

        print("\n🚨 LOCAL FILE INCLUSION DETECTED 🚨")

        print(f"IP: {request_info['ip']}")
        print(f"PATH: {request_info['path']}")
        print(f"QUERY: {request_info['query']}")
        print(f"FORM: {request_info['form']}")

        print("=" * 60)      

    # --------------------------------------------------
    # Remote File Inclusion (RFI)
    # --------------------------------------------------

    if detect_rfi(request_info):

        create_alert(
          "CRITICAL",
          "Remote File Inclusion (RFI)",
          f"IP={request_info['ip']} | "
          f"Path={request_info['path']} | "
          f"Query={request_info['query']} | "
          f"Form={request_info['form']}"
        )

        record_attack(
           request_info["ip"],
           "Remote File Inclusion"
        )

        print("\n🚨 REMOTE FILE INCLUSION DETECTED 🚨")

        print(f"IP: {request_info['ip']}")
        print(f"PATH: {request_info['path']}")
        print(f"QUERY: {request_info['query']}")
        print(f"FORM: {request_info['form']}")

        print("=" * 60)

    # --------------------------------------------------
    # Rate Limiting
    # --------------------------------------------------

    limited, count = check_rate_limit(request_info["ip"])

    if limited:

       create_alert(
           "WARNING",
           "Rate Limit Exceeded",
           f"IP={request_info['ip']} | Requests={count} in 60 seconds"
       )

       record_attack(
          request_info["ip"],
          "Rate Limit"
       )

       print("\n🚨 RATE LIMIT EXCEEDED 🚨")

       print(f"IP: {request_info['ip']}")
       print(f"Requests: {count}")

       print("=" * 60)    

@app.route("/ip-statistics")
def ip_statistics():
    return jsonify(get_ip_statistics())   

@app.route("/attack-dashboard")
def attack_dashboard():
    return render_template("ip_dashboard.html") 

from flask import jsonify
from app.services.ip_tracker import get_blocked_ips

@app.route("/blocked-ips")
def blocked_ips():

    return jsonify(get_blocked_ips())  

@app.route("/unblock/<ip>", methods=["POST"])
def unblock(ip):

    unblock_ip(ip)

    return jsonify({

        "message": f"{ip} has been unblocked."

    })    

if __name__ == "__main__":
    app.run(debug=True)


