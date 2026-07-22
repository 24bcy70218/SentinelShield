from datetime import datetime

blocked_ips = set()

ip_database = {}


def record_attack(ip, attack_type):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if ip not in ip_database:

        ip_database[ip] = {
            "count": 0,
            "last_seen": now,
            "types": {}
        }

    ip_database[ip]["count"] += 1
    ip_database[ip]["last_seen"] = now

    types = ip_database[ip]["types"]

    types[attack_type] = types.get(attack_type, 0) + 1

def block_ip(ip):
    blocked_ips.add(ip)

def unblock_ip(ip):
    blocked_ips.discard(ip)    


def is_blocked(ip):
    return ip in blocked_ips


def get_blocked_ips():
    return list(blocked_ips)    


def get_ip_statistics():

    result = []

   

    ATTACK_WEIGHTS = {

        "SQL Injection": 10,

        "Command Injection": 10,

        "Remote File Inclusion": 9,

        "Local File Inclusion": 8,

        "XSS": 7,

        "Directory Traversal": 6,

        "Rate Limit": 2

    } 

    for ip, data in ip_database.items():

        count = data["count"]

        threat_score = 0

        for attack_type, occurrences in data["types"].items():

         weight = ATTACK_WEIGHTS.get(attack_type, 1)

         threat_score += weight * occurrences

        if threat_score >= 50:
          block_ip(ip) 

        # Calculate risk level
        if threat_score < 15:

          risk = "Low"

        elif threat_score < 35:

          risk = "Medium"

        elif threat_score < 60:

          risk = "High"

        else:

          risk = "Critical"

        result.append({
          "ip": ip,
          "count": count,
          "last_seen": data["last_seen"],
          "types": data["types"],

          "threat_score": threat_score,
          "risk": risk,
          "blocked": is_blocked(ip)
          
        })

    result.sort(
        key=lambda x: x["count"],
        reverse=True
    )

    return result