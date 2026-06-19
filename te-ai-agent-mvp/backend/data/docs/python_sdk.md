# ThousandEyes Python SDK and Script Troubleshooting Guide

Use this document when customers share Python scripts that call ThousandEyes API v7 or ask for Python automation help.

## Common Python Support Requests

- Authentication errors.
- Wrong endpoint path.
- Invalid request body.
- JSON serialization issues.
- Pagination issues.
- Rate limiting.
- Timeout handling.
- Missing headers.
- SDK installation or usage questions.
- requests or httpx troubleshooting.

## Recommended API Base URL

Use:

https://api.thousandeyes.com/v7

## Required Headers

For most API calls:

Authorization: Bearer <TOKEN>
Accept: application/json

For requests with a JSON body:

Content-Type: application/json

## Token Handling

Best practices:

- Store bearer tokens in environment variables.
- Never hardcode bearer tokens in source code.
- Never print bearer tokens in logs.
- Never ask customers to share tokens.
- Use secret managers when possible.

Example:

```python
import os

TOKEN = os.environ["TE_BEARER_TOKEN"]
requests Best Practices

Use json=payload for JSON bodies.

Good:

response = requests.post(url, headers=headers, json=payload, timeout=30)

Avoid:

response = requests.post(url, headers=headers, data=payload)

unless the API specifically expects raw data.

Error Handling

Use:

response.raise_for_status()

Capture sanitized response body:

try:
    response.raise_for_status()
except requests.HTTPError:
    print(response.status_code)
    print(response.text)
    raise

Do not log secrets.

Timeout Handling

Always set a timeout:

requests.get(url, headers=headers, timeout=30)

Avoid calls without timeouts because scripts can hang indefinitely.

429 Rate Limit Handling

When status code is 429:

Check Retry-After header.
Sleep before retrying.
Use exponential backoff.
Avoid tight loops.
Reduce request frequency.

Example:

if response.status_code == 429:
    retry_after = int(response.headers.get("Retry-After", "5"))
    time.sleep(retry_after)
Pagination

For list endpoints:

Check API documentation for pagination fields.
Do not assume all results arrive in one response.
Continue requesting pages until no next page/token remains.
Avoid unbounded loops.
Common Script Mistakes
Missing Bearer prefix in Authorization header.
Using HTTP instead of HTTPS.
Using wrong API version.
Wrong endpoint path.
Wrong HTTP method.
Passing JSON as data instead of json.
Missing Content-Type for POST/PATCH/PUT.
Not handling 401, 403, 404, or 429.
Not setting timeout.
Hardcoding secrets.
Printing customer-sensitive data.
Support Engineer Review Checklist

When reviewing customer Python scripts:

Check base URL.
Check endpoint path.
Check HTTP method.
Check Authorization header.
Check Accept and Content-Type headers.
Check request payload structure.
Check query parameters.
Check timeout.
Check error handling.
Check retry/backoff logic.
Check pagination.
Check secret handling.
Evidence to Collect
Python version.
requests/httpx version.
Sanitized script.
Sanitized request URL.
HTTP method.
Sanitized request body.
Response status code.
Response body.
Timestamp.
Account group / aid.
