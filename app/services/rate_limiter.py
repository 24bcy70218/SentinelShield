import time

request_log = {}
alerted_ips = {}

WINDOW_SECONDS = 60
MAX_REQUESTS = 30


def check_rate_limit(ip):

    now = time.time()

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [
        t for t in request_log[ip]
        if now - t < WINDOW_SECONDS
    ]

    request_log[ip].append(now)

    count = len(request_log[ip])

    # Reset alert when traffic returns to normal
    if count <= MAX_REQUESTS:
        alerted_ips[ip] = False
        return False, count

    # First time exceeding the limit
    if not alerted_ips.get(ip, False):
        alerted_ips[ip] = True
        return True, count

    # Already alerted
    return False, count