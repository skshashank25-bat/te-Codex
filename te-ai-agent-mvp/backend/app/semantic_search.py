from typing import Any

from .embedding.ollama_provider import OllamaEmbeddingProvider
from .vector_store import ChromaVectorStore


DEFAULT_RESULT_LIMIT = 5


class SemanticSearch:
    """
    Semantic retrieval over the local ChromaDB index.
    """

    def __init__(
        self,
        embedding_provider: OllamaEmbeddingProvider | None = None,
        vector_store: ChromaVectorStore | None = None,
    ) -> None:
        self.embedding_provider = (
            embedding_provider or OllamaEmbeddingProvider()
        )

        self.vector_store = (
            vector_store or ChromaVectorStore()
        )

    def search(
        self,
        query: str,
        limit: int = DEFAULT_RESULT_LIMIT,
        where: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Embed a natural-language query and return the most
        semantically similar documentation chunks.
        """
        clean_query = query.strip()

        if not clean_query:
            raise ValueError("query cannot be empty")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        query_embedding = self.embedding_provider.embed(
            clean_query
        )

        matches = self.vector_store.query(
            query_embedding=query_embedding,
            limit=limit,
            where=where,
        )

        return matches


def search_semantic_docs(
    query: str,
    limit: int = DEFAULT_RESULT_LIMIT,
) -> list[dict[str, Any]]:
    """
    Convenience function for simple semantic retrieval.
    """
    searcher = SemanticSearch()

    return searcher.search(
        query=query,
        limit=limit,
    )