from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection


DEFAULT_CHROMA_PATH = Path("data/chroma")
DEFAULT_COLLECTION_NAME = "thousandeyes_support_docs"


class ChromaVectorStore:
    """
    Persistent ChromaDB storage for documentation chunks.

    Embeddings are supplied by the caller. This class does not call
    Ollama or any other embedding provider.
    """

    def __init__(
        self,
        persist_path: Path | str = DEFAULT_CHROMA_PATH,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        self.persist_path = Path(persist_path)
        self.collection_name = collection_name

        self.persist_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.persist_path)
        )

        self.collection: Collection = self._get_or_create_collection()

    def _get_or_create_collection(self) -> Collection:
        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={
                "description": (
                    "ThousandEyes support documentation chunks"
                ),
                "hnsw:space": "cosine",
            },
        )

    def count(self) -> int:
        """Return the number of records in the collection."""
        return self.collection.count()

    def upsert_chunks(
        self,
        chunks: list[dict[str, Any]],
        embeddings: list[list[float]],
    ) -> None:
        """
        Insert or update chunks and their embeddings.

        Each chunk is expected to contain:
        - chunk_id
        - content
        - source
        - document_title
        - heading
        - section_chunk_number
        - character_count
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings"
            )

        if not chunks:
            return

        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, str | int | float | bool]] = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_id = str(chunk.get("chunk_id", "")).strip()
            content = str(chunk.get("content", "")).strip()

            if not chunk_id:
                raise ValueError("Every chunk must contain a chunk_id")

            if not content:
                raise ValueError(
                    f"Chunk {chunk_id} does not contain content"
                )

            if not embedding:
                raise ValueError(
                    f"Chunk {chunk_id} does not contain an embedding"
                )

            ids.append(chunk_id)
            documents.append(content)

            metadatas.append(
                {
                    "source": str(chunk.get("source", "unknown")),
                    "document_title": str(
                        chunk.get("document_title", "Unknown")
                    ),
                    "heading": str(
                        chunk.get("heading", "Introduction")
                    ),
                    "section_chunk_number": int(
                        chunk.get("section_chunk_number", 1)
                    ),
                    "character_count": int(
                        chunk.get("character_count", len(content))
                    ),
                }
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(
        self,
        query_embedding: list[float],
        limit: int = 5,
        where: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Return the nearest chunks for a supplied query embedding.
        """
        if not query_embedding:
            raise ValueError("query_embedding cannot be empty")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        available_records = self.count()

        if available_records == 0:
            return []

        result_limit = min(limit, available_records)

        query_args: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": result_limit,
            "include": [
                "documents",
                "metadatas",
                "distances",
            ],
        }

        if where:
            query_args["where"] = where

        results = self.collection.query(**query_args)

        ids = self._first_result_list(results.get("ids"))
        documents = self._first_result_list(results.get("documents"))
        metadatas = self._first_result_list(results.get("metadatas"))
        distances = self._first_result_list(results.get("distances"))

        matches: list[dict[str, Any]] = []

        for index, chunk_id in enumerate(ids):
            distance = (
                float(distances[index])
                if index < len(distances)
                else None
            )

            similarity = (
                max(0.0, min(1.0, 1.0 - distance))
                if distance is not None
                else None
            )

            matches.append(
                {
                    "chunk_id": chunk_id,
                    "content": (
                        documents[index]
                        if index < len(documents)
                        else ""
                    ),
                    "metadata": (
                        metadatas[index]
                        if index < len(metadatas)
                        else {}
                    ),
                    "distance": distance,
                    "similarity": similarity,
                }
            )

        return matches

    def get(
        self,
        chunk_id: str,
    ) -> dict[str, Any] | None:
        """Retrieve one chunk by its ID."""
        clean_chunk_id = chunk_id.strip()

        if not clean_chunk_id:
            raise ValueError("chunk_id cannot be empty")

        result = self.collection.get(
            ids=[clean_chunk_id],
            include=["documents", "metadatas"],
        )

        ids = result.get("ids") or []

        if not ids:
            return None

        documents = result.get("documents") or []
        metadatas = result.get("metadatas") or []

        return {
            "chunk_id": ids[0],
            "content": documents[0] if documents else "",
            "metadata": metadatas[0] if metadatas else {},
        }

    def delete(self, chunk_ids: list[str]) -> None:
        """Delete selected chunks by ID."""
        clean_ids = [
            chunk_id.strip()
            for chunk_id in chunk_ids
            if chunk_id.strip()
        ]

        if clean_ids:
            self.collection.delete(ids=clean_ids)

    def reset(self) -> None:
        """
        Delete and recreate the collection.

        Use this before rebuilding the complete index.
        """
        try:
            self.client.delete_collection(
                name=self.collection_name
            )
        except Exception as exc:
            # Chroma may raise when the collection does not exist.
            if "does not exist" not in str(exc).lower():
                raise

        self.collection = self._get_or_create_collection()

    @staticmethod
    def _first_result_list(value: Any) -> list[Any]:
        """
        Chroma query results are grouped once per query vector.

        This project sends one query vector, so return the first group.
        """
        if not isinstance(value, list) or not value:
            return []

        first = value[0]

        return first if isinstance(first, list) else []