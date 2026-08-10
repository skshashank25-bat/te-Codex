import re
from .models import Workflow, Source
from .knowledge import find_endpoint
from .openapi_loader import search_operations
from .docs_loader import search_docs
from .semantic_search import search_semantic_docs

ERROR_INTENT_PATTERNS = {
    400: [
        r"\bbad request\b",
        r"\bmalformed request\b",
        r"\binvalid json\b",
        r"\bmissing required field\b",
        r"\binvalid parameter\b",
        r"\bschema mismatch\b",
    ],
    401: [
        r"\bunauthorized\b",
        r"\bbearer token\b",
        r"\btoken rejected\b",
        r"\btoken expired\b",
        r"\bexpired token\b",
        r"\binvalid token\b",
        r"\brevoked token\b",
        r"\bauthentication failed\b",
        r"\bauthentication error\b",
        r"\bnot authenticated\b",
    ],
    403: [
        r"\bforbidden\b",
        r"\bpermission denied\b",
        r"\baccess denied\b",
        r"\binsufficient permission\b",
        r"\binsufficient permissions\b",
        r"\binsufficient role\b",
        r"\binsufficient scope\b",
        r"\bnot authorized\b",
    ],
    404: [
        r"\bnot found\b",
        r"\bresource missing\b",
        r"\bresource does not exist\b",
        r"\bendpoint does not exist\b",
        r"\bwrong endpoint\b",
    ],
    405: [
        r"\bmethod not allowed\b",
        r"\bwrong http method\b",
        r"\bwrong method\b",
    ],
    429: [
        r"\btoo many requests\b",
        r"\brate limit\b",
        r"\brate limited\b",
        r"\brate limiting\b",
        r"\bthrottled\b",
        r"\bthrottling\b",
        r"\bretry-after\b",
    ],
    500: [
        r"\binternal server error\b",
        r"\bserver error\b",
        r"\bplatform error\b",
        r"\bbackend error\b",
    ],
    503: [
        r"\bservice unavailable\b",
        r"\btemporarily unavailable\b",
        r"\btemporary service outage\b",
        r"\bmaintenance\b",
    ],
}

ERROR_MAP = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    429: "Too Many Requests",
    500: "Internal Server Error",
    503: "Service Unavailable",
}


class MockLLMProvider:
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
    def _detect_error_codes(self, user_input: str) -> list[int]:
        """
        Detect API error codes from explicit status codes or
        natural-language error symptoms.
        """

        matched_codes: list[int] = []

        # Explicit status codes have the strongest signal.
        for code in ERROR_MAP:
            if re.search(rf"\b{code}\b", user_input):
                matched_codes.append(code)

        # Also detect natural-language descriptions.
        for code, patterns in ERROR_INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(
                    pattern,
                    user_input,
                    re.IGNORECASE,
                ):
                    if code not in matched_codes:
                        matched_codes.append(code)

                    break

        return matched_codes
    

    def _related_docs(self, user_input: str, limit: int = 3) -> list[dict]:
        """
        Retrieve related documentation.

        Semantic retrieval is preferred.
        Keyword retrieval is used as a fallback if semantic search
        is unavailable or returns no useful results.
        """

        try:
            semantic_results = search_semantic_docs(
                user_input,
                limit=limit,
            )

            if semantic_results:
                normalized_results = []

                for result in semantic_results:
                    metadata = result.get("metadata", {})

                    normalized_results.append(
                        {
                            "title": metadata.get(
                                "document_title",
                                "Documentation",
                            ),
                            "filename": metadata.get(
                                "source",
                                "unknown",
                            ),
                            "heading": metadata.get(
                                "heading",
                                "Related Information",
                            ),
                            "snippet": result.get(
                                "content",
                                "",
                            ),
                            "similarity": result.get(
                                "similarity",
                            ),
                            "retrieval_type": "semantic",
                        }
                    )

                return normalized_results

        except Exception:
            # Semantic retrieval is an enhancement.
            # If Ollama or ChromaDB is unavailable, keep the
            # application functional using keyword retrieval.
            pass

        keyword_results = search_docs(
            user_input,
            limit=limit,
        )

        normalized_results = []

        for result in keyword_results:
            normalized_results.append(
                {
                    "title": result.get(
                        "title",
                        "Documentation",
                    ),
                    "filename": result.get(
                        "filename",
                        "unknown",
                    ),
                    "heading": None,
                    "snippet": result.get(
                        "snippet",
                        "",
                    ),
                    "similarity": None,
                    "retrieval_type": "keyword",
                }
            )

        return normalized_results

    def _format_related_docs(
        self,
        docs: list[dict],
    ) -> str:
        """
        Format semantic or keyword retrieval results into the
        existing Related Documentation Markdown section.
        """

        if not docs:
            return "No related local documentation found yet."

        sections = []

        for doc in docs:
            title = doc.get("title", "Documentation")
            heading = doc.get("heading")
            filename = doc.get("filename", "unknown")
            snippet = doc.get("snippet", "").strip()

            if heading:
                section_title = f"### {title} — {heading}"
            else:
                section_title = f"### {title}"

            section = (
                f"{section_title}\n\n"
                f"{snippet}\n\n"
                f"_Source: `{filename}`_"
            )

            sections.append(section)

        return "\n\n".join(sections)

    def _api_endpoint_answer(self, user_input: str, sources: list[Source]) -> str:
        endpoint = find_endpoint(user_input)
        operations = search_operations(user_input)
        docs = self._related_docs(user_input)

        if not endpoint and not operations:
            return f"""## Recommended API v7 Endpoint

I could not confidently match this ask to a known endpoint yet.

Please include the resource type, such as web tests, alerts, endpoint agents, or account groups.

## Sources
{self._source_lines(sources)}
"""

        if operations:
            operation = operations[0]
            method = operation["method"]
            path = operation["path"]
            description = operation["description"] or operation["summary"]

            parameter_lines = []
            for param in operation.get("parameters", []):
                required_text = "required" if param.get("required") else "optional"
                parameter_lines.append(
                    f"- `{param.get('name')}`: {param.get('in')} parameter, {required_text}, type `{param.get('schema_type')}`. {param.get('description')}"
                )

            if not parameter_lines:
                parameter_lines.append("- No parameters listed in OpenAPI sample.")

            response_lines = []
            for response in operation.get("responses", []):
                response_lines.append(
                    f"- `{response.get('status_code')}`: {response.get('description')}"
                )

            if not response_lines:
                response_lines.append("- No responses listed in OpenAPI sample.")

        else:
            method = endpoint["method"]
            path = endpoint["endpoint"]
            description = endpoint["description"]
            parameter_lines = ["- OpenAPI details not available yet for this endpoint."]
            response_lines = ["- OpenAPI response details not available yet for this endpoint."]

        related_documentation = self._format_related_docs(docs)

        return f"""## Recommended API v7 Endpoint

- Method: `{method}`
- Endpoint: `{path}`
- Use case: {description}

## Parameters

{chr(10).join(parameter_lines)}

## Sample Request

```bash
curl --request {method} "https://api.thousandeyes.com/v7{path}" \\
  --header "Authorization: Bearer <TOKEN>" \\
  --header "Accept: application/json"
```
## Related Documentation
{related_documentation}

## Responses

{chr(10).join(response_lines)}

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

    def _api_error_answer(
        self,
        user_input: str,
        sources: list[Source],
    ) -> str:
        docs = self._related_docs(user_input)
        matched_codes = self._detect_error_codes(user_input)

        if matched_codes:
            matched = [
                (code, ERROR_MAP[code])
                for code in matched_codes
            ]
        else:
            matched = [
                (
                    "unknown",
                    "No HTTP status code or known API error pattern was detected.",
                )
            ]

        lines = "\n".join([f"- `{code}`: {cause}" for code, cause in matched])

        related_documentation = self._format_related_docs(docs)

        return f"""## Troubleshooting Notes

Likely causes:

{lines}

## How to Verify

- Confirm URL starts with `https://api.thousandeyes.com/v7`.
- Confirm method matches the endpoint.
- Confirm `Authorization: Bearer <TOKEN>` is present and valid.
- Confirm role, scope, account group, and `aid` context.
- Capture sanitized request body, response body, timestamp, and request ID if present.

## Related Documentation

{related_documentation}

## Sources
{self._source_lines(sources)}
"""

    def _python_answer(
        self,
        user_input: str,
        sources: list[Source],
    ) -> str:
        docs = self._related_docs(user_input)

        related_documentation = self._format_related_docs(
            docs
        )

        return f"""## Python Script Review

Checklist:

- Use `https://api.thousandeyes.com/v7`.
- Use `Authorization: Bearer <TOKEN>`.
- Store tokens in environment variables.
- Use `json=payload` for JSON bodies.
- Add timeout, error handling, 429 retry logic, and pagination.

## Related Documentation

{related_documentation}

## Sources
{self._source_lines(sources)}
"""

    def _transaction_answer(
        self,
        user_input: str,
        sources: list[Source],
    ) -> str:
        docs = self._related_docs(
            user_input,
            limit=4,
        )

        related_documentation = self._format_related_docs(
            docs
        )

        return f"""## Transaction Script Review


Checklist:

- Use async / await consistently.
- Import from selenium-webdriver and thousandeyes.
- Wait for elements before clicking or typing.
- Prefer stable CSS selectors.
- Avoid fixed sleeps when possible.
- Use markers around important journey steps.
- Do not hardcode credentials.

## Related Documentation

{related_documentation}

## Sources
{self._source_lines(sources)}
"""

    def _general_answer(self, sources: list[Source]) -> str:
        return f"""## ThousandEyes Support Agent

I can help with API v7 endpoint selection, API error troubleshooting, Python script review, and Transaction JavaScript/Selenium script review.

## Sources
{self._source_lines(sources)}
"""
