import re

COMMAND_PATTERNS = [

    # Linux / Unix
    r";",
    r"\|\|",
    r"&&",
    r"\|",
    r"`.*?`",
    r"\$\(.+?\)",

    # Common Commands
    r"\bwhoami\b",
    r"\bid\b",
    r"\buname\b",
    r"\bcat\b",
    r"\bls\b",
    r"\bps\b",
    r"\bping\b",
    r"\bcurl\b",
    r"\bwget\b",
    r"\bnc\b",
    r"\bnetcat\b",

    # Windows Commands
    r"\bdir\b",
    r"\btype\b",
    r"\bcopy\b",
    r"\bmove\b",
    r"\bdel\b",
    r"\bipconfig\b",
    r"\btasklist\b",
    r"\bshutdown\b",
    r"\bpowershell\b",
    r"\bcmd\b"
]


def detect_command_injection(request_info):
    """
    Detect Command Injection payloads.
    """

    payload = ""

    for value in request_info.get("query", {}).values():
        payload += str(value) + " "

    for value in request_info.get("form", {}).values():
        payload += str(value) + " "

    for pattern in COMMAND_PATTERNS:

        if re.search(pattern, payload, re.IGNORECASE):

            return True

    return False