import re

TRAVERSAL_PATTERNS = [

    r"\.\./",
    r"\.\.\\",

    r"%2e%2e%2f",
    r"%2e%2e/",
    r"\.\.%2f",

    r"%2e%2e%5c",
    r"\.\.%5c",

    r"%252e%252e%252f",
    r"%252e%252e%255c"
]


def detect_directory_traversal(request_info):

    payload = ""

    for value in request_info.get("query", {}).values():
        payload += str(value) + " "

    for value in request_info.get("form", {}).values():
        payload += str(value) + " "

    for pattern in TRAVERSAL_PATTERNS:

        if re.search(pattern, payload, re.IGNORECASE):

            return True

    return False