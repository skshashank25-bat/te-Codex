from .models import Workflow, Source
from .knowledge import find_endpoint

ERROR_MAP = {
    400: "Malformed request, invalid JSON, missing required field, invalid query parameter, or body schema mismatch.",
    401: "Missing, expired, invalid, or revoked bearer token.",
    403: "Authenticated but insufficient role, scope, account group, or resource permission.",
    404: "Wrong endpoint path, wrong object ID, resource not visible, or API version mismatch.",
    405: "Wrong HTTP method for the endpoint.",
    429: "Rate limit exceeded. Honor Retry-After and add backoff.",
    500: "Possible platform-side error. Collect timestamp, endpoint, method, payload, response body, and request ID.",
    503: "Temporary service unavailability or maintenance.",
}


class MockLLMProvider:
    async def generate(self, user_input: str, workflow: Workflow, sources: list[Source]) -> str:
        if workflow == Workflow.api_endpoint:
            return self._api_endpoint_answer(user_input, sources)
        if workflow == Workflow.api_error:
            return self._api_error_answer(user_input, sources)
        if workflow == Workflow.python_script:
            return self._python_answer(sources)
        if workflow == Workflow.transaction_script:
            return self._transaction_answer(sources)
        return self._general_answer(sources)

    def _source_lines(self, sources: list[Source]) -> str:
        return "\n".join([f"- {s.title}: {s.url}" for s in sources])

    def _api_endpoint_answer(self, user_input: str, sources: list[Source]) -> str:
        endpoint = find_endpoint(user_input)

        if not endpoint:
            return f"""## Recommended API v7 Endpoint

I could not confidently match this ask to a known endpoint yet.

Please include the resource type, such as web tests, alerts, endpoint agents, or account groups.

## Sources
{self._source_lines(sources)}
"""

        method = endpoint["method"]
        path = endpoint["endpoint"]
        description = endpoint["description"]

        return f"""## Recommended API v7 Endpoint

- Method: `{method}`
- Endpoint: `{path}`
- Use case: {description}

## Sample Request

```bash
curl --request {method} "https://api.thousandeyes.com/v7{path}" \\
  --header "Authorization: Bearer <TOKEN>" \\
  --header "Accept: application/json"
```

## Sample JSON Response

```json
{{
  "example": "Representative placeholder. Replace with official OpenAPI response schema in the next phase."
}}
```

## Common Troubleshooting Notes

- `401`: Check bearer token validity.
- `403`: Check role, scope, and account group access.
- `404`: Check endpoint path, object ID, API version, and account group visibility.
- `429`: Add retry handling and honor `Retry-After`.

## Sources
{self._source_lines(sources)}
"""

    def _api_error_answer(self, user_input: str, sources: list[Source]) -> str:
        matched = []
        for code, cause in ERROR_MAP.items():
            if str(code) in user_input:
                matched.append((code, cause))

        if not matched:
            matched = [("unknown", "No explicit status code detected.")]

        lines = "\n".join([f"- `{code}`: {cause}" for code, cause in matched])

        return f"""## Troubleshooting Notes

Likely causes:

{lines}

## How to Verify

- Confirm URL starts with `https://api.thousandeyes.com/v7`.
- Confirm method matches the endpoint.
- Confirm `Authorization: Bearer <TOKEN>` is present and valid.
- Confirm role, scope, account group, and `aid` context.
- Capture sanitized request body, response body, timestamp, and request ID if present.

## Sources
{self._source_lines(sources)}
"""

    def _python_answer(self, sources: list[Source]) -> str:
        return f"""## Python Script Review

Checklist:

- Use `https://api.thousandeyes.com/v7`.
- Use `Authorization: Bearer <TOKEN>`.
- Store tokens in environment variables.
- Use `json=payload` for JSON bodies.
- Add timeout, error handling, 429 retry logic, and pagination.

## Sources
{self._source_lines(sources)}
"""

    def _transaction_answer(self, sources: list[Source]) -> str:
        return f"""## Transaction Script Review

Checklist:

- Use `async` / `await` consistently.
- Import from `selenium-webdriver` and `thousandeyes`.
- Wait for elements before clicking or typing.
- Prefer stable CSS selectors.
- Avoid fixed sleeps when possible.
- Use markers around important journey steps.
- Do not hardcode credentials.

## Sources
{self._source_lines(sources)}
"""

    def _general_answer(self, sources: list[Source]) -> str:
        return f"""## ThousandEyes Support Agent

I can help with API v7 endpoint selection, API error troubleshooting, Python script review, and Transaction JavaScript/Selenium script review.

## Sources
{self._source_lines(sources)}
"""
