"""
AIService interface.

A provider-agnostic abstraction over whichever LLM API FLUX ends up using
for the FLUX assistant chat experience. Keeping this as an interface lets
us swap providers (Anthropic, OpenAI, local model, etc.) without touching
API routes or the RAG pipeline.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ChatMessage:
    role: str  # "user" | "assistant" | "system"
    content: str


class AIService(ABC):
    @abstractmethod
    def generate_response(
        self, messages: list[ChatMessage], context: str | None = None
    ) -> str:
        """Generate a grounded chat response, optionally given retrieved context."""
        raise NotImplementedError


class NotImplementedAIService(AIService):
    def generate_response(
        self, messages: list[ChatMessage], context: str | None = None
    ) -> str:
        raise NotImplementedError(
            "AI assistant service is not implemented yet (planned: Milestone 5)."
        )
