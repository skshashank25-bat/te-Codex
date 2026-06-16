from .models import Source

OFFICIAL_SOURCES = [
    Source(
        title="ThousandEyes API v7 - Cisco DevNet",
        url="https://developer.cisco.com/docs/thousandeyes/",
        snippet="Official API v7 documentation. RESTful API using standard HTTP methods and response codes.",
        authority="official",
    ),
    Source(
        title="ThousandEyes API v7 Overview",
        url="https://developer.cisco.com/docs/thousandeyes/overview/",
        snippet="Official overview and authentication guidance for API v7 requests.",
        authority="official",
    ),
    Source(
        title="ThousandEyes Transaction Scripting Reference",
        url="https://docs.thousandeyes.com/product-documentation/browser-synthetics/transaction-tests/transaction-scripting-reference",
        snippet="Official JavaScript/Selenium transaction scripting reference.",
        authority="official",
    ),
    Source(
        title="Creating Robust Transaction Scripts",
        url="https://docs.thousandeyes.com/product-documentation/browser-synthetics/transaction-tests/development-guide/robust-transaction-scripts",
        snippet="Official guidance for optimizing and troubleshooting Transaction scripts.",
        authority="official",
    ),
]
API_ENDPOINTS = {
    "web tests": {
        "method": "GET",
        "endpoint": "/tests/web",
        "description": "Retrieve web tests.",
    },
    "alerts": {
        "method": "GET",
        "endpoint": "/alerts",
        "description": "Retrieve alerts or alert-related resources.",
    },
    "endpoint agents": {
        "method": "GET",
        "endpoint": "/endpoint-agents",
        "description": "Retrieve Endpoint Agents.",
    },
    "account groups": {
        "method": "GET",
        "endpoint": "/account-groups",
        "description": "Retrieve account groups.",
    },
}


def find_endpoint(query: str):
    q = query.lower()
    for key, value in API_ENDPOINTS.items():
        if key in q:
            return value
    return None

class StubRetriever:
    """Replace with vector search over docs, OpenAPI specs, TAC KBs, and MCP results."""

    async def search(self, query: str, workflow: str) -> list[Source]:
        if workflow == "transaction_script":
            return [s for s in OFFICIAL_SOURCES if "Transaction" in s.title or "Robust" in s.title]
        return OFFICIAL_SOURCES[:2]
