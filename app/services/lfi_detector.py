import re

LFI_PATTERNS = [

    # PHP wrappers
    r"php://",
    r"php://filter",
    r"php://input",
    r"file://",

    # Sensitive Linux files
    r"/etc/passwd",
    r"/etc/shadow",
    r"/proc/self/environ",

    # Windows files
    r"boot\.ini",
    r"win\.ini",
    r"system32",

    # PHP source files
    r"\.php$",
    r"\.inc$",
    r"\.config$"
]


def detect_lfi(request_info):

    payload = ""

    for value in request_info.get("query", {}).values():
        payload += str(value) + " "

    for value in request_info.get("form", {}).values():
        payload += str(value) + " "

    for pattern in LFI_PATTERNS:

        if re.search(pattern, payload, re.IGNORECASE):
            return True

    return False