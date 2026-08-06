from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Base interface for embedding providers.

    Every embedding provider should implement these methods.
    """

    @abstractmethod
    def embed(self, text: str):
        """
        Return an embedding vector for one piece of text.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_many(self, texts: list[str]):
        """
        Return embedding vectors for multiple pieces of text.
        """
        raise NotImplementedError