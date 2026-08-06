import json
import os
from collections.abc import Sequence
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .base import EmbeddingProvider


DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_EMBEDDING_MODEL = "embeddinggemma"


class OllamaEmbeddingProvider(EmbeddingProvider):
    """
    Generate embeddings using an Ollama model running locally.

    This implementation uses Python's standard library so it does not
    depend on httpx, requests, or other third-party HTTP clients.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
        base_url: str | None = None,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.model_name = model_name
        self.base_url = (
            base_url
            or os.getenv("OLLAMA_BASE_URL")
            or DEFAULT_OLLAMA_URL
        ).rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _request_json(
        self,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        if payload is None:
            request = Request(
                url,
                method="GET",
                headers={"Accept": "application/json"},
            )
        else:
            body = json.dumps(payload).encode("utf-8")
            request = Request(
                url,
                data=body,
                method="POST",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            )

        try:
            with urlopen(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                response_body = response.read().decode("utf-8")

        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Ollama returned HTTP {exc.code}: {error_body}"
            ) from exc

        except URLError as exc:
            raise RuntimeError(
                f"Could not connect to Ollama at {self.base_url}. "
                "Confirm that the Ollama application is running."
            ) from exc

        try:
            result = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Ollama returned a response that was not valid JSON"
            ) from exc

        if not isinstance(result, dict):
            raise RuntimeError("Ollama returned an unexpected response")

        return result

    def embed(self, text: str) -> list[float]:
        vectors = self.embed_many([text])

        if not vectors:
            raise RuntimeError("Ollama returned no embedding")

        return vectors[0]

    def embed_many(self, texts: Sequence[str]) -> list[list[float]]:
        clean_texts = [text.strip() for text in texts]

        if not clean_texts:
            return []

        if any(not text for text in clean_texts):
            raise ValueError("Cannot embed empty text")

        payload = self._request_json(
            "/api/embed",
            {
                "model": self.model_name,
                "input": clean_texts,
            },
        )

        embeddings = payload.get("embeddings")

        if not isinstance(embeddings, list):
            raise RuntimeError(
                "Ollama response did not contain an embeddings list"
            )

        if len(embeddings) != len(clean_texts):
            raise RuntimeError(
                "Ollama returned a different number of embeddings "
                "than requested"
            )

        vectors: list[list[float]] = []

        for embedding in embeddings:
            if not isinstance(embedding, list):
                raise RuntimeError("Ollama returned an invalid embedding")

            vectors.append([float(value) for value in embedding])

        return vectors

    def health_check(self) -> bool:
        try:
            self._request_json("/api/tags")
            return True
        except RuntimeError:
            return False

    @property
    def dimension(self) -> int:
        return len(self.embed("dimension check"))