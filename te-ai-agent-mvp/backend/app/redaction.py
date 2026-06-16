import re

TOKEN_PATTERNS = [
    re.compile(r"Authorization:\s*Bearer\s+[A-Za-z0-9._\-]+", re.I),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}", re.I),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^'\"\s,}]+"),
]


def redact_sensitive(text: str) -> tuple[str, bool]:
    redacted = text
    changed = False
    for pattern in TOKEN_PATTERNS:
        new = pattern.sub(lambda m: m.group(0).split()[0] + " <REDACTED>" if "Bearer" in m.group(0) else "<REDACTED_SECRET>", redacted)
        if new != redacted:
            changed = True
            redacted = new
    return redacted, changed
