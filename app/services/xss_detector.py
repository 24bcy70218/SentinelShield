import re

XSS_PATTERNS = [
    r"<script.*?>.*?</script>",
    r"javascript:",
    r"onerror\s*=",
    r"onload\s*=",
    r"onclick\s*=",
    r"onmouseover\s*=",
    r"<img",
    r"<svg",
    r"<iframe",
    r"<body",
    r"document\.cookie",
    r"document\.location",
    r"window\.location",
    r"alert\s*\(",
    r"confirm\s*\(",
    r"prompt\s*\("
]

def detect_xss(request_info):

    payload = ""

    payload += str(request_info.get("query", {}))
    payload += " "
    payload += str(request_info.get("form", {}))

    for pattern in XSS_PATTERNS:
        if re.search(pattern, payload, re.IGNORECASE):
            return True

    return False