# ThousandEyes API v7 Authentication

ThousandEyes API v7 requests use OAuth2 Bearer token authentication.

Requests should include:

Authorization: Bearer <TOKEN>
Accept: application/json

For requests with JSON bodies, include:

Content-Type: application/json

Never ask customers to share bearer tokens, client secrets, passwords, cookies, or private keys.

Common authentication-related errors:

- 401 Unauthorized: missing, expired, invalid, or revoked token.
- 403 Forbidden: token is valid, but the user lacks role, scope, or account group access.
- 429 Too Many Requests: rate limit exceeded; honor Retry-After when present.

Support engineers should collect:

- HTTP method
- Full sanitized URL
- Sanitized request body
- Response status code
- Response body
- Timestamp
- Account group / aid context
