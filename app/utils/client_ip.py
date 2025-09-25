import re
from fastapi import Request

SHORT_CODE_RE = re.compile(r"^[A-Za-z0-9_-]{4,64}$")


def extract_client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    client = request.client
    return client.host if client else "unknown"
