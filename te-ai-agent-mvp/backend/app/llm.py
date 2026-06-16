from .models import Workflow, Source

SYSTEM_INSTRUCTIONS = """
You are a Cisco ThousandEyes Support Engineer Agent.
Use official ThousandEyes documentation first. Do not invent endpoint details.
If exact endpoint/schema is not available from retrieved context or MCP, say what is missing.
Never request or expose bearer tokens, passwords, cookies, or client secrets.
Prefer sanitized curl reproduction for API troubleshooting.
"""

ERROR_MAP = {
    400: "Malformed request, invalid JSON, missing required field, invalid query parameter, or body schema mismatch.",
    401: "Missing, expired, invalid, or revoked bearer token; also check repeated unauthorized attempts.",
    403: "Authenticated but insufficient role, scope, account group, or resource permission.",
    404: "Wrong endpoint path, wrong object ID, resource not visible in account group, or API version mismatch.",
    405: "Wrong HTTP method for the endpoint.",
    406: "Accept header mismatch.",
    415: "Wrong Content-Type or unsupported request body format.",
    429: "Rate limit exceeded. Honor Retry-After if present and add backoff.",
    500: "Possible platform-side error. Collect timestamp, endpoint, method, sanitized payload, response body, and request ID if present.",
    503: "Temporary service unavailability or maintenance. Retry later and escalate if persistent.",
}


class MockLLMProvider:
    """Replace with approved LLM provider. This deterministic version is useful for MVP testing."""

    async def generate(self, user_input: str, workflow: Workflow, sources: list[Source]) -> str:
        if workflow == Workflow.api_endpoint:
            return self._api_endpoint_answer(user_input, sources)
        if workflow == Workflow.api_error:
            return self._api_error_answer(user_input, sources)
        if workflow == Workflow.python_script:
            return self._python_answer(user_input, sources)
        if workflow == Workflow.transaction_script:
            return self._transaction_answer(user_input, sources)
        return self._general_answer(sources)

    def _source_lines(self, sources: list[Source]) -> str:
        return "\n".join([f"- {s.title}: {s.url}" for s in sources])

    def _api_endpoint_answer(self, user_input: str, sources: list[Source]) -> str:
        return f"""## Recommended API v7 Endpoint

I need the RAG/OpenAPI lookup or MCP result to provide the exact method/path for this ask. The scaffold is ready to connect that retrieval step.

What I would return after retrieval:

- Method: `<GET|POST|PUT|PATCH|DELETE>`
- Endpoint: `/v7/<resource>`
- Use case: matched to the customer's ask
- Required parameters: from OpenAPI schema
- Optional parameters: from OpenAPI schema
- Auth/role notes: from official docs or MCP metadata

## Sample Request

```bash
curl --request GET "https://api.thousandeyes.com/v7/<endpoint>" \\
  --header "Authorization: Bearer <TOKEN>" \\
  --header "Accept: application/json"
```

## Sample JSON Response

```json
{{
  "example": "Replace with official OpenAPI/doc sample or clearly label representative output"
}}
```

## Retrieval Sources To Use
{self._source_lines(sources)}
"""

    def _api_error_answer(self, user_input: str, sources: list[Source]) -> str:
        matched = []
        for code, cause in ERROR_MAP.items():
            if str(code) in user_input:
                matched.append((code, cause))
        if not matched:
            matched = [("unknown", "No explicit status code detected. Inspect response body fields such as timestamp, httpStatus, errors, and path.")]

        lines = "\n".join([f"- `{code}`: {cause}" for code, cause in matched])
        return f"""## Troubleshooting Notes

Likely causes based on the provided input:

{lines}

## How to Verify

- Confirm full URL starts with `https://api.thousandeyes.com/v7`.
- Confirm method matches the API operation.
- Confirm `Authorization: Bearer <TOKEN>` is present and not expired.
- Confirm `Accept: application/json` and `Content-Type: application/json` for requests with a JSON body.
- Confirm account group / `aid` context and user role/scope.
- Capture sanitized request body, response body, timestamp, and request ID if present.

## Fix Pattern

```bash
curl --request <METHOD> "https://api.thousandeyes.com/v7/<endpoint>" \\
  --header "Authorization: Bearer <TOKEN>" \\
  --header "Accept: application/json" \\
  --header "Content-Type: application/json" \\
  --data '{{}}'
```

## Sources
{self._source_lines(sources)}
"""

    def _python_answer(self, user_input: str, sources: list[Source]) -> str:
        return f"""## Python Script Review

Checklist applied:

- Use `https://api.thousandeyes.com/v7` as the base URL.
- Use `Authorization: Bearer <TOKEN>`.
- Keep tokens in environment variables, not source code.
- Use `json=payload`, not `data=payload`, for JSON API bodies.
- Set request timeouts.
- Call `response.raise_for_status()` and print sanitized error bodies.
- Add 429 retry handling using `Retry-After` when present.
- Add pagination handling for list endpoints when applicable.

## Safer Request Helper

```python
import os
import time
import requests

BASE_URL = "https://api.thousandeyes.com/v7"
TOKEN = os.environ["TE_BEARER_TOKEN"]

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {{TOKEN}}",
    "Accept": "application/json",
    "Content-Type": "application/json",
})

def te_request(method, path, **kwargs):
    url = f"{{BASE_URL}}{{path}}"
    kwargs.setdefault("timeout", 30)

    for _ in range(3):
        response = session.request(method, url, **kwargs)
        if response.status_code == 429:
            time.sleep(int(response.headers.get("Retry-After", "5")))
            continue
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            try:
                body = response.json()
            except ValueError:
                body = response.text
            raise RuntimeError({{
                "status_code": response.status_code,
                "url": url,
                "error": body,
            }}) from exc
        return None if response.status_code == 204 else response.json()

    raise RuntimeError("Request failed after retries due to rate limiting")
```

## Sources
{self._source_lines(sources)}
"""

    def _transaction_answer(self, user_input: str, sources: list[Source]) -> str:
        return f"""## Transaction Script Review

Checklist applied for ThousandEyes Transaction JavaScript/Selenium scripts:

- Import from `selenium-webdriver` and `thousandeyes` correctly.
- Use `async` / `await` consistently.
- Configure timeouts based on `test.getSettings()`.
- Prefer reliable selectors: stable IDs, data attributes, then CSS; avoid brittle XPath when possible.
- Wait for elements before clicking or typing.
- Avoid fixed sleeps unless no better signal exists.
- Use markers around key user-journey steps.
- Keep credentials in the ThousandEyes credential repository, not in script text.
- For custom JavaScript, remember browser-page JavaScript context is separate from transaction control code.

## Starter Pattern

```javascript
import {{ By, until }} from 'selenium-webdriver';
import {{ driver, test }} from 'thousandeyes';

runScript();

async function runScript() {{
  await configureDriver();
  const settings = test.getSettings();

  await driver.get(settings.url);

  const loginButton = await driver.wait(
    until.elementLocated(By.css('[data-testid="login"]')),
    10000
  );

  await driver.wait(until.elementIsVisible(loginButton), 10000);
  await loginButton.click();
}}

async function configureDriver() {{
  const settings = test.getSettings();
  await driver.manage().setTimeouts({{
    implicit: Math.floor(settings.timeout / 2) * 1000,
  }});
}}
```

## Sources
{self._source_lines(sources)}
"""

    def _general_answer(self, sources: list[Source]) -> str:
        return f"""## ThousandEyes Support Agent

I can help with API v7 endpoint selection, API error troubleshooting, Python script review, and Transaction JavaScript/Selenium script review.

## Sources
{self._source_lines(sources)}
"""
