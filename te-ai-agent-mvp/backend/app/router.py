import re

from .models import Workflow


TRANSACTION_PATTERNS = [
    r"\btransaction test\b",
    r"\btransaction script\b",
    r"\bselenium\b",
    r"\bxpath\b",
    r"\bcss selector\b",
    r"\bselector\b",
    r"\bchromium\b",
    r"\bbrowser upgrade\b",
    r"\bbrowser rollout\b",
    r"\bhar\b",
    r"\bwaterfall\b",
    r"\belement not found\b",
    r"\belement not clickable\b",
    r"\bjavascript bundle\b",
    r"\bpage rendering\b",
    r"\bscript broke\b",
    r"\bscript failed\b",
]

API_ERROR_PATTERNS = [
    r"\b400\b",
    r"\b401\b",
    r"\b403\b",
    r"\b404\b",
    r"\b405\b",
    r"\b429\b",
    r"\b500\b",
    r"\b503\b",
    r"\bunauthorized\b",
    r"\bforbidden\b",
    r"\btoo many requests\b",
    r"\brate limit\b",
    r"\brate limited\b",
    r"\btoken rejected\b",
    r"\btoken expired\b",
    r"\binvalid token\b",
    r"\bbearer token\b",
    r"\bauthentication failed\b",
    r"\bauthentication error\b",
    r"\bpermission denied\b",
    r"\baccess denied\b",
]

PYTHON_PATTERNS = [
    r"\bpython\b",
    r"\brequests\b",
    r"\bhttpx\b",
    r"\bresponse\.json\b",
    r"\bimport requests\b",
    r"\bimport httpx\b",
    r"\btraceback\b",
    r"\bpython script\b",
]

API_ENDPOINT_PATTERNS = [
    r"\bapi endpoint\b",
    r"\bendpoint\b",
    r"\bretrieve\b",
    r"\blist\b",
    r"\bget\b",
    r"\bcreate\b",
    r"\bupdate\b",
    r"\bdelete\b",
    r"\bapi v7\b",
    r"\bendpoint agents\b",
    r"\btransaction tests\b",
    r"\bweb tests\b",
    r"\balerts\b",
    r"\baccount groups\b",
]


def _matches_any(text: str, patterns: list[str]) -> bool:
    """
    Return True when the input matches at least one routing pattern.
    """
    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in patterns
    )


def detect_workflow(user_input: str) -> Workflow:
    """
    Detect the most appropriate support workflow.

    Priority matters:
    1. Transaction/browser troubleshooting
    2. API errors
    3. Python script review
    4. API endpoint lookup
    5. General
    """

    text = user_input.strip()

    if not text:
        return Workflow.general

    if _matches_any(text, TRANSACTION_PATTERNS):
        return Workflow.transaction_script

    if _matches_any(text, API_ERROR_PATTERNS):
        return Workflow.api_error

    if _matches_any(text, PYTHON_PATTERNS):
        return Workflow.python_script

    if _matches_any(text, API_ENDPOINT_PATTERNS):
        return Workflow.api_endpoint

    return Workflow.general

def route_workflow(user_input: str) -> Workflow:
    """
    Backward-compatible wrapper used by the FastAPI application.
    """
    return detect_workflow(user_input)