from .models import Workflow


def route_workflow(text: str) -> Workflow:
    t = text.lower()

    if any(x in t for x in [
    "selenium",
    "webdriver",
    "driver.",
    "by.css",
    "by.xpath",
    "await ",
    "async function",
    "import { driver",
    "import { test",
    "runscript()"
]):
        return Workflow.transaction_script

    if any(x in t for x in ["import requests", "requests.", "python", "traceback", "raise_for_status", "urllib", "httpx"]):
        return Workflow.python_script

    if any(x in t for x in ["401", "403", "404", "429", "500", "503", "status code", "error", "httpstatus", "unauthorized", "forbidden"]):
        return Workflow.api_error

    if any(x in t for x in [
        "endpoint", "api", "curl",
        "get ", "post ", "put ", "patch ", "delete ",
        "list", "create", "update", "retrieve", "fetch", "show",
        "test", "tests", "web test", "web tests",
        "agent", "agents", "alert", "alerts",
        "account group", "aid"
    ]):
        return Workflow.api_endpoint

    return Workflow.general