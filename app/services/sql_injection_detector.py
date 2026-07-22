import re

SQLI_PATTERNS = [
    r"\bOR\b\s+\d+=\d+",
    r"\bAND\b\s+\d+=\d+",
    r"UNION\s+SELECT",
    r"SELECT.+FROM",
    r"INSERT\s+INTO",
    r"UPDATE.+SET",
    r"DELETE\s+FROM",
    r"DROP\s+TABLE",
    r"EXEC(\s|\+)+",
    r"xp_cmdshell",
    r"INFORMATION_SCHEMA",
    r"SLEEP\s*\(",
    r"BENCHMARK\s*\(",
    r"(--|#)"
]


def detect_sql_injection(request_info):
    """
    Returns True if SQL Injection is detected.
    """

    payload = ""

    for value in request_info.get("query", {}).values():
       payload += str(value) + " "

    for value in request_info.get("form", {}).values():
       payload += str(value) + " "

    payload = payload.upper()

    for pattern in SQLI_PATTERNS:

        if re.search(pattern, payload, re.IGNORECASE):

            return True

    return False