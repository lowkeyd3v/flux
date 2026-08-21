"""
AIService interface and implementations (Milestone 5).

A provider-agnostic abstraction over LLM chat generation and grounded
synthesis for the FLUX Scheme Assistant.
"""

import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests

from app.core.config import get_settings

logger = logging.getLogger(__name__)


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


class GroundedExtractiveAIService(AIService):
    """
    Deterministic, highly-grounded synthesis engine.

    Used when no external LLM API key is configured or when offline.
    Extracts key financial facts, eligibility rules, required documents,
    and application steps directly from retrieved context chunks without
    hallucination.
    """

    def generate_response(
        self, messages: list[ChatMessage], context: str | None = None
    ) -> str:
        if not context:
            return "No relevant government scheme information was found to answer this question."

        user_query = ""
        for m in reversed(messages):
            if m.role == "user":
                user_query = m.content
                break

        query_lower = user_query.lower()

        # Parse context chunks by source / section
        sections = self._parse_context_sections(context)
        if not sections:
            return context.strip()

        # Build clean, structured markdown response
        output_parts: list[str] = []

        primary_scheme = list(sections.keys())[0] if sections else "Government Scheme"
        scheme_sections = sections.get(primary_scheme, {})

        # 1. Headline summary
        overview = scheme_sections.get("Overview & Benefits") or scheme_sections.get("Financial Assistance & Subsidies")
        if overview:
            # Clean up raw prefixes
            cleaned_overview = re.sub(r"\[Source:[^\]]+\]", "", overview).strip()
            output_parts.append(f"### {primary_scheme}\n{cleaned_overview}\n")
        else:
            output_parts.append(f"### {primary_scheme}\n")

        # 2. Specific intent-based focus
        # If user asked about eligibility
        if any(w in query_lower for w in ["eligible", "eligibility", "who can", "criteria"]):
            elig = scheme_sections.get("Eligibility Criteria")
            if elig:
                cleaned_elig = re.sub(r"\[Source:[^\]]+\]", "", elig).strip()
                output_parts.append(f"**Eligibility Requirements:**\n{cleaned_elig}\n")

        # If user asked about documents
        if any(w in query_lower for w in ["document", "documents", "paper", "papers", "aadhaar", "pan"]):
            docs = scheme_sections.get("Required Documents")
            if docs:
                cleaned_docs = re.sub(r"\[Source:[^\]]+\]", "", docs).strip()
                output_parts.append(f"**Documents Required:**\n{cleaned_docs}\n")

        # If user asked about application / how to apply
        if any(w in query_lower for w in ["apply", "how to", "process", "portal", "steps", "where"]):
            steps = scheme_sections.get("Application Process")
            if steps:
                cleaned_steps = re.sub(r"\[Source:[^\]]+\]", "", steps).strip()
                output_parts.append(f"**Step-by-Step Application Guide:**\n{cleaned_steps}\n")

        # If user asked about loan amount, subsidy, interest rate, cashback
        if any(w in query_lower for w in ["amount", "subsidy", "interest", "cashback", "benefit", "money", "tranche", "shishu", "kishore", "tarun"]):
            benefits = scheme_sections.get("Financial Assistance & Subsidies")
            if benefits and benefits != overview:
                cleaned_ben = re.sub(r"\[Source:[^\]]+\]", "", benefits).strip()
                output_parts.append(f"**Financial Details & Subsidies:**\n{cleaned_ben}\n")

        # If generic / overview question (or if none of the specific filters matched), include structured checklist
        if len(output_parts) <= 1:
            if "Eligibility Criteria" in scheme_sections:
                output_parts.append(f"**Key Eligibility:**\n{scheme_sections['Eligibility Criteria']}\n")
            if "Financial Assistance & Subsidies" in scheme_sections and "Financial Assistance & Subsidies" != overview:
                output_parts.append(f"**Benefits & Subsidies:**\n{scheme_sections['Financial Assistance & Subsidies']}\n")
            if "Required Documents" in scheme_sections:
                output_parts.append(f"**Documents Needed:**\n{scheme_sections['Required Documents']}\n")
            if "Application Process" in scheme_sections:
                output_parts.append(f"**How to Apply:**\n{scheme_sections['Application Process']}\n")

        # Mention other matched schemes if multiple were retrieved
        other_schemes = [s for s in sections.keys() if s != primary_scheme]
        if other_schemes:
            output_parts.append(
                f"\n*Also related: {', '.join(other_schemes)} — ask for details on any of these schemes.*"
            )

        return "\n".join(output_parts).strip()

    @staticmethod
    def _parse_context_sections(context: str) -> dict[str, dict[str, str]]:
        """Parses chunk text formatted with [Source: ... | Section: ...] headers."""
        sections_by_scheme: dict[str, dict[str, str]] = {}
        chunks = context.split("\n\n")

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue

            header_match = re.search(r"\[Source:\s*([^\|]+)\s*\|\s*Section:\s*([^\|]+)(?:\|\s*Portal:\s*([^\s\]]+))?\]", chunk)
            if header_match:
                source = header_match.group(1).strip()
                section = header_match.group(2).strip()
                content = chunk[header_match.end():].strip()
            else:
                source = "General Information"
                section = "Details"
                content = chunk

            if source not in sections_by_scheme:
                sections_by_scheme[source] = {}
            sections_by_scheme[source][section] = content

        return sections_by_scheme


class LLMAIService(AIService):
    """
    Real LLM API service for external generative models (e.g. OpenAI / Gemini).
    Falls back to GroundedExtractiveAIService if external call fails.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.fallback_engine = GroundedExtractiveAIService()

    def generate_response(
        self, messages: list[ChatMessage], context: str | None = None
    ) -> str:
        if not self.api_key:
            return self.fallback_engine.generate_response(messages, context)

        api_messages = []
        if context:
            api_messages.append({
                "role": "system",
                "content": (
                    "You are FLUX Scheme Assistant. Answer the user's question using ONLY the provided "
                    "official government scheme context below. Be concise, respectful, and actionable. "
                    "If the answer cannot be found in the context, clearly say so.\n\n"
                    f"--- OFFICIAL CONTEXT ---\n{context}\n--- END CONTEXT ---"
                ),
            })

        for m in messages:
            api_messages.append({"role": m.role, "content": m.content})

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": api_messages,
                    "temperature": 0.2,
                },
                timeout=10,
            )
            if response.ok:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.warning("LLM API returned status %s: %s", response.status_code, response.text[:200])
        except Exception as e:
            logger.warning("LLM API call failed with exception: %s", e)

        # Fallback to local grounded extractive synthesis
        return self.fallback_engine.generate_response(messages, context)


class NotImplementedAIService(AIService):
    def generate_response(
        self, messages: list[ChatMessage], context: str | None = None
    ) -> str:
        raise NotImplementedError(
            "AI assistant service is not implemented yet."
        )


def get_ai_service() -> AIService:
    """Factory used as a FastAPI dependency."""
    settings = get_settings()
    if settings.LLM_API_KEY:
        return LLMAIService(api_key=settings.LLM_API_KEY)
    return GroundedExtractiveAIService()
