import re

RFI_PATTERNS = [

    # Remote protocols
    r"http://",
    r"https://",
    r"ftp://",

    # Protocol-relative URL
    r"^//",

    # Common malicious file types
    r"\.php$",
    r"\.asp$",
    r"\.aspx$",
    r"\.jsp$",

    # Common remote hosting services
    r"raw\.githubusercontent\.com",
    r"pastebin\.com",
    r"gist\.github\.com",

    # Generic IP-based URLs
    r"https?://\d{1,3}(?:\.\d{1,3}){3}"
]


def detect_rfi(request_info):

    payload = ""

    for value in request_info.get("query", {}).values():
        payload += str(value) + " "

    for value in request_info.get("form", {}).values():
        payload += str(value) + " "

    for pattern in RFI_PATTERNS:

        if re.search(pattern, payload, re.IGNORECASE):
            return True

    return False