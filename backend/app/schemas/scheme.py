"""
Pydantic schemas for Government Scheme RAG and recommendations (Milestone 5).
"""

import uuid
from pydantic import BaseModel, Field


class RetrievedChunkSchema(BaseModel):
    source: str
    section: str
    content: str
    score: float
    official_url: str | None = None


class SchemeSummarySchema(BaseModel):
    id: str
    name: str
    ministry: str
    category: str
    max_benefit: str
    subsidy_info: str
    collateral_required: bool
    short_description: str
    official_url: str


class SchemeDetailSchema(SchemeSummarySchema):
    target_audience: str
    eligibility: list[str]
    benefits: list[str]
    documents_required: list[str]
    application_steps: list[str]


class SchemeQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Natural language query about government schemes")
    vendor_id: uuid.UUID | None = Field(default=None, description="Optional vendor ID to personalize context")
    top_k: int = Field(default=4, ge=1, le=10, description="Number of context chunks to retrieve")


class SchemeQueryResponse(BaseModel):
    query: str
    answer: str
    sources: list[RetrievedChunkSchema]
    matched_schemes: list[SchemeSummarySchema]
    suggested_followups: list[str] = []


class RecommendedSchemeSchema(BaseModel):
    scheme: SchemeSummarySchema
    match_reason: str
    recommended_action: str


class VendorRecommendationsResponse(BaseModel):
    vendor_id: uuid.UUID
    vendor_name: str
    recommendations: list[RecommendedSchemeSchema]
