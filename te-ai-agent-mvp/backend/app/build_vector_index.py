from pathlib import Path

from .chunker import chunk_directory
from .embedding.ollama_provider import OllamaEmbeddingProvider
from .vector_store import ChromaVectorStore


DOCS_DIRECTORY = Path("data/docs")

MAX_CHARS = 1200
OVERLAP_CHARS = 180

BATCH_SIZE = 8


def build_vector_index() -> None:
    """
    Build the persistent ChromaDB index from the local Markdown
    documentation corpus.
    """

    print("Loading and chunking documentation...")

    chunks = chunk_directory(
        DOCS_DIRECTORY,
        max_chars=MAX_CHARS,
        overlap_chars=OVERLAP_CHARS,
    )

    if not chunks:
        raise RuntimeError(
            f"No documentation chunks found in {DOCS_DIRECTORY}"
        )

    print(f"Chunks found: {len(chunks)}")

    print("\nConnecting to Ollama...")

    embedding_provider = OllamaEmbeddingProvider()

    if not embedding_provider.health_check():
        raise RuntimeError(
            "Ollama is not available. "
            "Start Ollama before rebuilding the vector index."
        )

    print("Ollama: OK")
    print(f"Embedding model: {embedding_provider.model_name}")

    print("\nOpening ChromaDB...")

    vector_store = ChromaVectorStore()

    print(
        "Existing records:",
        vector_store.count(),
    )

    print("\nResetting vector collection...")

    vector_store.reset()

    print("Collection reset complete.")

    total_chunks = len(chunks)

    print(
        f"\nGenerating embeddings in batches of {BATCH_SIZE}..."
    )

    for start in range(0, total_chunks, BATCH_SIZE):
        end = min(
            start + BATCH_SIZE,
            total_chunks,
        )

        batch = chunks[start:end]

        # Include the heading in the text presented to the embedding model.
        # This gives the embedding additional semantic context while the
        # original chunk content remains unchanged in ChromaDB.
        embedding_texts = [
            (
                f"{chunk['document_title']}\n"
                f"{chunk['heading']}\n\n"
                f"{chunk['content']}"
            )
            for chunk in batch
        ]

        embeddings = embedding_provider.embed_many(
            embedding_texts
        )

        vector_store.upsert_chunks(
            chunks=batch,
            embeddings=embeddings,
        )

        print(
            f"Indexed {end}/{total_chunks} chunks"
        )

    final_count = vector_store.count()

    print("\nVector index build complete.")
    print("Expected records:", total_chunks)
    print("Stored records:", final_count)

    if final_count != total_chunks:
        raise RuntimeError(
            "Vector index count does not match chunk count"
        )

    print("\nIndex verification: PASSED")


if __name__ == "__main__":
    build_vector_index()