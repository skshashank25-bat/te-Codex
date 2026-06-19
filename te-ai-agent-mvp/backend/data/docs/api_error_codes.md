# ThousandEyes API Error Codes Support Guide

Use this document when customers ask about ThousandEyes API v7 HTTP errors, response codes, failed API calls, or troubleshooting API responses.

## 400 Bad Request

Common causes:

- Invalid JSON body.
- Missing required field.
- Invalid query parameter.
- Wrong data type.
- Request body does not match schema.
- Unsupported filter or pagination parameter.

How to verify:

- Validate JSON syntax.
- Compare request body against API schema.
- Check required fields.
- Check query parameter spelling and values.
- Confirm Content-Type: application/json for JSON bodies.

## 401 Unauthorized

Common causes:

- Missing bearer token.
- Expired bearer token.
- Invalid bearer token.
- Revoked bearer token.
- Authorization header malformed.

How to verify:

- Confirm Authorization: Bearer <TOKEN> header exists.
- Confirm token is active.
- Confirm token was copied correctly.
- Confirm no extra quotes or spaces were added.
- Do not ask the customer to share the token.

## 403 Forbidden

Common causes:

- User is authenticated but lacks required role.
- Missing scope.
- Account group restriction.
- Resource is not visible to the user.
- Token belongs to a user without access.

How to verify:

- Confirm the same user can access the resource in UI.
- Confirm account group / aid context.
- Confirm user role and permissions.
- Confirm the resource belongs to the expected account group.

## 404 Not Found

Common causes:

- Wrong endpoint path.
- Wrong API version.
- Invalid object ID.
- Resource was deleted.
- Resource exists but is not visible in the selected account group.

How to verify:

- Confirm URL starts with https://api.thousandeyes.com/v7.
- Confirm endpoint path.
- Confirm object ID.
- Confirm account group / aid context.
- Compare with UI visibility.

## 405 Method Not Allowed

Common causes:

- Wrong HTTP method.
- Using POST when endpoint requires GET.
- Using PATCH/PUT/DELETE on unsupported resource.

How to verify:

- Check OpenAPI operation method.
- Confirm curl uses the documented method.

## 406 Not Acceptable

Common causes:

- Missing or incorrect Accept header.
- Client requests unsupported response format.

How to verify:

- Use Accept: application/json.

## 415 Unsupported Media Type

Common causes:

- Missing Content-Type header for JSON request.
- Incorrect request body format.

How to verify:

- Use Content-Type: application/json for JSON bodies.
- Use json=payload in Python requests instead of data=payload when sending JSON.

## 429 Too Many Requests

Common causes:

- API rate limit exceeded.
- Too many requests in a short period.
- Script lacks backoff or retry logic.

How to verify:

- Check response headers.
- Honor Retry-After if present.
- Add exponential backoff.
- Reduce request frequency.
- Avoid tight loops.

## 500 Internal Server Error

Common causes:

- Temporary platform-side issue.
- Backend service error.
- Unexpected API failure.

How to verify:

- Retry once after short delay.
- Capture timestamp, endpoint, method, sanitized payload, response body, and request ID if present.
- Escalate if persistent.

## 503 Service Unavailable

Common causes:

- Temporary service unavailability.
- Maintenance.
- Transient platform issue.

How to verify:

- Retry later.
- Check status or maintenance notifications.
- Escalate if persistent.

## Evidence to Collect

- HTTP method.
- Full sanitized URL.
- Request headers without secrets.
- Sanitized request body.
- Response status code.
- Response body.
- Timestamp.
- Account group / aid.
- User role context.
- Request ID if present.
