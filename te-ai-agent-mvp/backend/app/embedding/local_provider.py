from collections.abc import Sequence

from sentence_transformers import SentenceTransformer

from .base import EmbeddingProvider


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class LocalEmbeddingProvider(EmbeddingProvider):
    """
    Generate embeddings locally with Sentence Transformers.

    The model is downloaded the first time it is used and then cached
    on the machine for later runs.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        clean_text = text.strip()

        if not clean_text:
            raise ValueError("Cannot embed empty text")

        vector = self.model.encode(
            clean_text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_many(self, texts: Sequence[str]) -> list[list[float]]:
        clean_texts = [text.strip() for text in texts]

        if not clean_texts:
            return []

        if any(not text for text in clean_texts):
            raise ValueError("Cannot embed empty text")

        vectors = self.model.encode(
            clean_texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return vectors.tolist()

    @property
    def dimension(self) -> int:
        dimension = self.model.get_sentence_embedding_dimension()

        if dimension is None:
            raise RuntimeError(
                f"Could not determine embedding dimension for {self.model_name}"
            )

        return dimension