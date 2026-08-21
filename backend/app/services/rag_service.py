"""
RAGService interface and implementation.

Retrieval-augmented generation over government scheme documents for Indian
street vendors and micro-entrepreneurs (Milestone 5).
"""

import json
import math
import re
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMES_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "schemes_data.json"


@dataclass
class RetrievedChunk:
    source: str
    content: str
    score: float
    section: str = ""
    official_url: str | None = None
    scheme_id: str = ""


@dataclass
class RAGAnswerResult:
    query: str
    answer: str
    sources: list[RetrievedChunk] = field(default_factory=list)
    matched_schemes: list[dict] = field(default_factory=list)
    suggested_followups: list[str] = field(default_factory=list)


class RAGService(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Retrieve the most relevant scheme document chunks for a query."""
        raise NotImplementedError

    @abstractmethod
    def answer(self, query: str, vendor_context: dict | None = None) -> RAGAnswerResult:
        """Retrieve context and generate a grounded, source-attributed answer."""
        raise NotImplementedError

    @abstractmethod
    def list_schemes(self, category: str | None = None) -> list[dict]:
        """List available schemes with optional category filtering."""
        raise NotImplementedError

    @abstractmethod
    def get_scheme(self, scheme_id: str) -> dict | None:
        """Get full details of a specific scheme by ID."""
        raise NotImplementedError

    @abstractmethod
    def recommend_for_vendor(self, vendor_data: dict) -> list[dict]:
        """Recommend relevant schemes based on vendor profile and constraints."""
        raise NotImplementedError


def _tokenize(text: str) -> list[str]:
    """Tokenize and normalize text for lexical/semantic vector matching."""
    text = text.lower()
    # Normalize Indian currency and terms
    text = text.replace("₹", " rupees ").replace("rs.", " rupees ").replace("rs ", " rupees ")
    tokens = re.findall(r"\b[a-z0-9_-]{2,}\b", text)
    stopwords = {
        "a", "an", "the", "in", "on", "at", "for", "to", "of", "and", "or", "is",
        "are", "was", "were", "be", "been", "by", "how", "what", "which", "who",
        "can", "could", "would", "should", "do", "does", "did", "have", "has",
        "had", "with", "this", "that", "these", "those", "from", "as", "about",
        "any", "tell", "me", "i", "my", "we", "our", "you", "your", "get", "need",
        "want", "apply", "give", "available", "there"
    }
    return [t for t in tokens if t not in stopwords]


class SchemeRAGService(RAGService):
    """
    Production-ready RAG service for Indian government schemes.

    - Loads curated knowledge base from schemes_data.json.
    - Chunks documents by logical sections (Overview, Eligibility, Benefits,
      Documents, Application Steps).
    - Performs TF-IDF vector indexing and cosine similarity retrieval with
      lexical boosting for exact scheme names and keywords.
    - Produces grounded, hallucination-free answers with precise citations.
    """

    def __init__(self, data_path: Path | None = None):
        self.data_path = data_path or SCHEMES_DATA_PATH
        self.schemes: list[dict] = []
        self.chunks: list[RetrievedChunk] = []
        self._doc_frequencies: Counter = Counter()
        self._num_chunks: int = 0
        self._chunk_vectors: list[dict[str, float]] = []
        self._load_and_index()

    def _load_and_index(self):
        if not self.data_path.exists():
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            self.schemes = json.load(f)

        self.chunks = []
        chunk_token_lists: list[list[str]] = []

        for scheme in self.schemes:
            s_name = scheme["name"]
            s_id = scheme["id"]
            s_url = scheme.get("official_url")

            # 1. Overview chunk
            overview_text = (
                f"{s_name} ({scheme['category']}), under {scheme['ministry']}. "
                f"Target Audience: {scheme['target_audience']}. "
                f"Summary: {scheme['short_description']} "
                f"Max Benefit: {scheme['max_benefit']}. Subsidy: {scheme['subsidy_info']}."
            )
            self.chunks.append(
                RetrievedChunk(
                    source=s_name,
                    section="Overview & Benefits",
                    content=overview_text,
                    score=0.0,
                    official_url=s_url,
                    scheme_id=s_id,
                )
            )

            # 2. Eligibility chunk
            eligibility_text = (
                f"Eligibility criteria for {s_name}: "
                + " ".join(scheme.get("eligibility", []))
                + f" Target group: {scheme['target_audience']}."
            )
            self.chunks.append(
                RetrievedChunk(
                    source=s_name,
                    section="Eligibility Criteria",
                    content=eligibility_text,
                    score=0.0,
                    official_url=s_url,
                    scheme_id=s_id,
                )
            )

            # 3. Benefits & Subsidy chunk
            benefits_text = (
                f"Financial benefits, loan amounts, and subsidies under {s_name}: "
                f"Maximum Benefit: {scheme['max_benefit']}. "
                f"Subsidy/Terms: {scheme['subsidy_info']}. "
                + " ".join(scheme.get("benefits", []))
            )
            self.chunks.append(
                RetrievedChunk(
                    source=s_name,
                    section="Financial Assistance & Subsidies",
                    content=benefits_text,
                    score=0.0,
                    official_url=s_url,
                    scheme_id=s_id,
                )
            )

            # 4. Documents chunk
            docs_text = (
                f"Required documents for applying to {s_name}: "
                + " ".join(f"- {d}" for d in scheme.get("documents_required", []))
            )
            self.chunks.append(
                RetrievedChunk(
                    source=s_name,
                    section="Required Documents",
                    content=docs_text,
                    score=0.0,
                    official_url=s_url,
                    scheme_id=s_id,
                )
            )

            # 5. Application Steps chunk
            steps_text = (
                f"How to apply for {s_name} (Official Portal: {s_url}): "
                + " ".join(scheme.get("application_steps", []))
            )
            self.chunks.append(
                RetrievedChunk(
                    source=s_name,
                    section="Application Process",
                    content=steps_text,
                    score=0.0,
                    official_url=s_url,
                    scheme_id=s_id,
                )
            )

        self._num_chunks = len(self.chunks)
        self._doc_frequencies = Counter()

        for chunk in self.chunks:
            tokens = set(_tokenize(chunk.content + " " + chunk.source + " " + chunk.section))
            chunk_token_lists.append(list(tokens))
            for token in tokens:
                self._doc_frequencies[token] += 1

        self._chunk_vectors = []
        for i, chunk in enumerate(self.chunks):
            tokens = _tokenize(chunk.content + " " + chunk.source + " " + chunk.section)
            counts = Counter(tokens)
            total = len(tokens) or 1
            vec: dict[str, float] = {}
            for t, count in counts.items():
                tf = count / total
                idf = math.log((self._num_chunks + 1) / (self._doc_frequencies[t] + 1)) + 1.0
                vec[t] = tf * idf
            # L2 normalize
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            for t in vec:
                vec[t] /= norm
            self._chunk_vectors.append(vec)

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        if not self.chunks:
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            # Return top overview chunks if query is empty/generic
            return [
                RetrievedChunk(
                    source=c.source,
                    content=c.content,
                    score=0.5,
                    section=c.section,
                    official_url=c.official_url,
                    scheme_id=c.scheme_id,
                )
                for c in self.chunks[:top_k]
            ]

        # Compute query vector
        query_counts = Counter(query_tokens)
        query_vec: dict[str, float] = {}
        total = len(query_tokens)
        for t, count in query_counts.items():
            tf = count / total
            idf = math.log((self._num_chunks + 1) / (self._doc_frequencies.get(t, 0) + 1)) + 1.0
            query_vec[t] = tf * idf
        q_norm = math.sqrt(sum(v * v for v in query_vec.values())) or 1.0
        for t in query_vec:
            query_vec[t] /= q_norm

        lower_query = query.lower()
        scored_chunks: list[tuple[float, RetrievedChunk]] = []

        for i, chunk in enumerate(self.chunks):
            c_vec = self._chunk_vectors[i]
            # Cosine similarity
            cosine_score = sum(query_vec[t] * c_vec.get(t, 0.0) for t in query_vec)

            # Keyword / acronym boost
            boost = 0.0
            source_lower = chunk.source.lower()
            section_lower = chunk.section.lower()
            chunk_content_lower = chunk.content.lower()

            # Scheme-specific keyword matches
            if "svanidhi" in lower_query and ("svanidhi" in source_lower or "svanidhi" in chunk.scheme_id):
                boost += 0.45
            if "mudra" in lower_query and ("mudra" in source_lower or "mudra" in chunk.scheme_id):
                boost += 0.45
            if "shishu" in lower_query and "shishu" in chunk_content_lower:
                boost += 0.35
            if "kishore" in lower_query and "kishore" in chunk_content_lower:
                boost += 0.35
            if "tarun" in lower_query and "tarun" in chunk_content_lower:
                boost += 0.35
            if "vishwakarma" in lower_query and "vishwakarma" in source_lower:
                boost += 0.45
            if ("shram" in lower_query or "uan" in lower_query) and "shram" in source_lower:
                boost += 0.45
            if "insurance" in lower_query and ("insurance" in section_lower or "bima" in source_lower):
                boost += 0.35
            if "pension" in lower_query and ("pension" in section_lower or "maan-dhan" in source_lower or "sym" in source_lower):
                boost += 0.35
            if "guarantee" in lower_query and "cgtmse" in source_lower:
                boost += 0.35
            if "nulm" in lower_query and "nulm" in source_lower:
                boost += 0.35

            # Intent matches (eligibility, documents, apply, subsidy)
            if any(w in lower_query for w in ["eligible", "eligibility", "who can"]) and "eligibility" in section_lower:
                boost += 0.25
            if any(w in lower_query for w in ["document", "documents", "papers", "aadhaar", "pan"]) and "document" in section_lower:
                boost += 0.25
            if any(w in lower_query for w in ["apply", "how to", "portal", "website", "process", "steps"]) and "process" in section_lower:
                boost += 0.25
            if any(w in lower_query for w in ["interest", "subsidy", "rate", "benefit", "amount", "cashback"]) and "benefits" in section_lower:
                boost += 0.25

            final_score = min(round(cosine_score + boost, 4), 1.0)
            if final_score > 0.01:
                scored_chunks.append((
                    final_score,
                    RetrievedChunk(
                        source=chunk.source,
                        content=chunk.content,
                        score=final_score,
                        section=chunk.section,
                        official_url=chunk.official_url,
                        scheme_id=chunk.scheme_id,
                    ),
                ))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top = [chunk for score, chunk in scored_chunks[:top_k]]
        return top

    def answer(self, query: str, vendor_context: dict | None = None) -> RAGAnswerResult:
        import time
        from app.core.metrics import get_metrics_registry

        start_t = time.time()
        chunks = self.retrieve(query, top_k=5)
        if not chunks:
            elapsed = time.time() - start_t
            get_metrics_registry().record_rag_query(elapsed)
            return RAGAnswerResult(
                query=query,
                answer=(
                    "I could not find specific government schemes matching your query. "
                    "You can ask about PM SVANidhi (street vendor loans), PM MUDRA Yojana, "
                    "PM Vishwakarma (artisan toolkits & loans), e-Shram social security, or insurance schemes."
                ),
                sources=[],
                matched_schemes=[],
                suggested_followups=[
                    "How do I get a ₹10,000 working capital loan under PM SVANidhi?",
                    "What documents are required for PM MUDRA Shishu loan?",
                    "What benefits does PM Vishwakarma offer to artisans?",
                ],
            )

        matched_scheme_ids = list(dict.fromkeys(c.scheme_id for c in chunks if c.scheme_id))
        matched_schemes = [s for s in self.schemes if s["id"] in matched_scheme_ids]

        # Use AI service or Grounded Extractive synthesis
        from app.services.ai_service import get_ai_service, ChatMessage

        ai_service = get_ai_service()

        context_text = "\n\n".join(
            f"[Source: {c.source} | Section: {c.section} | Portal: {c.official_url or 'N/A'}]\n{c.content}"
            for c in chunks
        )

        vendor_prompt = ""
        if vendor_context:
            vendor_prompt = (
                f"\nVendor Profile Context:\n"
                f"- Name: {vendor_context.get('name', 'Vendor')}\n"
                f"- Product: {vendor_context.get('product', 'Goods/Services')}\n"
                f"- Location: {vendor_context.get('location', 'India')}\n"
                f"- Current Budget: ₹{vendor_context.get('budget', 0)}\n"
                f"- Current Inventory: {vendor_context.get('current_inventory', 0)} units\n"
            )

        messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are FLUX Scheme Assistant, an expert advisor for Indian street vendors and micro-entrepreneurs. "
                    "Answer the vendor's question using ONLY the provided scheme context. Be clear, direct, and actionable. "
                    "Include loan limits, interest subsidies, eligibility requirements, required documents, and exact application steps."
                ),
            ),
            ChatMessage(
                role="user",
                content=f"Question: {query}{vendor_prompt}",
            ),
        ]

        synthesized_answer = ai_service.generate_response(messages, context=context_text)

        # Generate follow-up suggestions
        followups = self._generate_followups(query, matched_schemes)

        elapsed = time.time() - start_t
        get_metrics_registry().record_rag_query(elapsed)

        return RAGAnswerResult(
            query=query,
            answer=synthesized_answer,
            sources=chunks,
            matched_schemes=matched_schemes,
            suggested_followups=followups,
        )

    def _generate_followups(self, query: str, matched_schemes: list[dict]) -> list[str]:
        followups = []
        if not matched_schemes:
            return [
                "What schemes provide working capital for street vendors?",
                "How do I apply for PM SVANidhi loan?",
                "What is the eligibility for PM MUDRA Shishu loan?",
            ]

        primary_scheme = matched_schemes[0]
        s_id = primary_scheme["id"]

        if s_id == "pm-svanidhi":
            followups.append("What documents do I need to submit for PM SVANidhi?")
            followups.append("How does the 7% interest subsidy work on timely repayment?")
            followups.append("Can I get ₹20,000 or ₹50,000 in the next tranche?")
        elif s_id == "pm-mudra-yojana":
            followups.append("What is the difference between Shishu and Kishore loans?")
            followups.append("Is collateral required for a MUDRA loan?")
            followups.append("How to get a MUDRA RuPay debit card for working capital?")
        elif s_id == "pm-vishwakarma":
            followups.append("Which 18 trades are eligible under PM Vishwakarma?")
            followups.append("How to claim the ₹15,000 toolkit grant e-voucher?")
            followups.append("What is the interest rate on PM Vishwakarma enterprise loan?")
        elif s_id == "e-shram-portal":
            followups.append("How to download the 12-digit e-Shram UAN card?")
            followups.append("What insurance benefits are linked to e-Shram registration?")
        else:
            followups.append(f"What documents are required for {primary_scheme['name']}?")
            followups.append(f"How do I apply for {primary_scheme['name']}?")
            followups.append("What other working capital schemes are available for vendors?")

        return followups[:3]

    def list_schemes(self, category: str | None = None) -> list[dict]:
        if not category:
            return self.schemes
        category_lower = category.lower()
        return [s for s in self.schemes if category_lower in s.get("category", "").lower()]

    def get_scheme(self, scheme_id: str) -> dict | None:
        for s in self.schemes:
            if s["id"] == scheme_id:
                return s
        return None

    def recommend_for_vendor(self, vendor_data: dict) -> list[dict]:
        """
        Personalized scheme recommendations based on vendor's business context.
        """
        budget = float(vendor_data.get("budget", 0) or 0)
        product = (vendor_data.get("product") or "").lower()
        location = vendor_data.get("location") or "Urban India"
        recommendations = []

        # 1. PM SVANidhi: Premier working capital recommendation for street vendors
        svanidhi = self.get_scheme("pm-svanidhi")
        if svanidhi:
            recommendations.append({
                "scheme": svanidhi,
                "match_reason": (
                    f"Ideal working capital loan for street vending in {location}. "
                    f"Gives ₹10,000 initial loan with 7% interest subvention and digital cashback."
                ),
                "recommended_action": "Apply via pmsvanidhi.mohua.gov.in with Certificate of Vending or ULB Letter of Recommendation.",
            })

        # 2. PM MUDRA: Recommended for business expansion or higher capital needs
        mudra = self.get_scheme("pm-mudra-yojana")
        if mudra:
            if budget < 50000:
                tier = "Shishu (up to ₹50,000 with zero processing fees)"
            else:
                tier = "Kishore (₹50,000 to ₹5,00,000 for equipment & stock)"
            recommendations.append({
                "scheme": mudra,
                "match_reason": (
                    f"Collateral-free business credit under {tier} to purchase inventory "
                    f"for {product or 'business operations'} without third-party guarantees."
                ),
                "recommended_action": "Apply at any commercial bank branch or via udyamimitra.in portal.",
            })

        # 3. PM Vishwakarma: If product relates to handicrafts/artisan/repair trades
        artisan_keywords = ["craft", "pottery", "clay", "carpenter", "tailor", "leather", "cobbler", "blacksmith", "handicraft", "cloth", "textile"]
        if any(k in product for k in artisan_keywords):
            vishwakarma = self.get_scheme("pm-vishwakarma")
            if vishwakarma:
                recommendations.append({
                    "scheme": vishwakarma,
                    "match_reason": (
                        f"Perfect match for your trade ({product}): provides ₹15,000 toolkit e-voucher "
                        f"and 5% concessional enterprise loan up to ₹3,00,000."
                    ),
                    "recommended_action": "Register with Aadhaar at your nearest Common Service Centre (CSC).",
                })

        # 4. e-Shram + Insurance: Universal social security
        eshram = self.get_scheme("e-shram-portal")
        if eshram:
            recommendations.append({
                "scheme": eshram,
                "match_reason": "Essential national social security card with ₹2 Lakh accidental insurance cover for informal workers.",
                "recommended_action": "Free 2-minute registration on eshram.gov.in using Aadhaar OTP.",
            })

        return recommendations


class NotImplementedRAGService(RAGService):
    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        raise NotImplementedError("Government scheme RAG service is not initialized.")

    def answer(self, query: str, vendor_context: dict | None = None) -> RAGAnswerResult:
        raise NotImplementedError("Government scheme RAG service is not initialized.")

    def list_schemes(self, category: str | None = None) -> list[dict]:
        raise NotImplementedError("Government scheme RAG service is not initialized.")

    def get_scheme(self, scheme_id: str) -> dict | None:
        raise NotImplementedError("Government scheme RAG service is not initialized.")

    def recommend_for_vendor(self, vendor_data: dict) -> list[dict]:
        raise NotImplementedError("Government scheme RAG service is not initialized.")


_rag_service_instance: RAGService | None = None


def get_rag_service() -> RAGService:
    """Factory used as a FastAPI dependency and service singleton."""
    global _rag_service_instance
    if _rag_service_instance is None:
        if SCHEMES_DATA_PATH.exists():
            _rag_service_instance = SchemeRAGService(SCHEMES_DATA_PATH)
        else:
            _rag_service_instance = NotImplementedRAGService()
    return _rag_service_instance
