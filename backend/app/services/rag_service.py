"""
RAGService interface.

Retrieval-augmented generation over government scheme documents.
Concrete implementation (embedding + vector store + retrieval) arrives
in Milestone 5. Kept independently replaceable from AIService so the
vector store (FAISS/ChromaDB) can be swapped without touching chat logic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    source: str
    content: str
    score: float


class RAGService(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Retrieve the most relevant scheme document chunks for a query."""
        raise NotImplementedError

    @abstractmethod
    def answer(self, query: str) -> str:
        """Retrieve context and generate a grounded, source-attributed answer."""
        raise NotImplementedError


class NotImplementedRAGService(RAGService):
    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        raise NotImplementedError(
            "Government scheme RAG service is not implemented yet (planned: Milestone 5)."
        )

    def answer(self, query: str) -> str:
        raise NotImplementedError(
            "Government scheme RAG service is not implemented yet (planned: Milestone 5)."
        )
