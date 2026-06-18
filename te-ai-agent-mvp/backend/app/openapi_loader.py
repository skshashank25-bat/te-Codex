import json
from pathlib import Path
from typing import Any


def load_openapi_spec(filename: str = "sample_openapi.json") -> dict[str, Any]:
    data_path = Path(__file__).resolve().parent.parent / "data" / filename

    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_operations(spec: dict[str, Any]) -> list[dict[str, Any]]:
    operations = []

    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method, operation in methods.items():
            method_upper = method.upper()

            parameters = []
            for param in operation.get("parameters", []):
                parameters.append(
                    {
                        "name": param.get("name"),
                        "in": param.get("in"),
                        "required": param.get("required", False),
                        "description": param.get("description", ""),
                        "schema_type": param.get("schema", {}).get("type"),
                    }
                )

            responses = []
            for status_code, response in operation.get("responses", {}).items():
                responses.append(
                    {
                        "status_code": status_code,
                        "description": response.get("description", ""),
                    }
                )

            operations.append(
                {
                    "method": method_upper,
                    "path": path,
                    "summary": operation.get("summary", ""),
                    "description": operation.get("description", ""),
                    "parameters": parameters,
                    "responses": responses,
                }
            )

    return operations


def search_operations(query: str, filename: str = "sample_openapi.json") -> list[dict[str, Any]]:
    q = query.lower()
    query_words = set(q.split())

    spec = load_openapi_spec(filename)
    operations = extract_operations(spec)

    scored_matches = []

    for operation in operations:
        searchable_text = " ".join(
            [
                operation["method"],
                operation["path"],
                operation["summary"],
                operation["description"],
            ]
        ).lower()

        score = 0

        if q in searchable_text:
            score += 10

        for word in query_words:
            if word in searchable_text:
                score += 1

        if score > 1:
            scored_matches.append((score, operation))

    scored_matches.sort(key=lambda item: item[0], reverse=True)

    return [operation for score, operation in scored_matches]