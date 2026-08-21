"""
Government scheme RAG & recommendations API routes (Milestone 5).

Endpoints for exploring Indian government schemes, asking natural language
questions with source-grounded RAG answers, and receiving personalized scheme
recommendations based on a vendor's business profile.
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.scheme import (
    RetrievedChunkSchema,
    SchemeDetailSchema,
    SchemeQueryRequest,
    SchemeQueryResponse,
    SchemeSummarySchema,
    VendorRecommendationsResponse,
)
from app.services.rag_service import get_rag_service, RAGService

router = APIRouter(tags=["schemes"])


@router.get("/schemes", response_model=list[SchemeSummarySchema])
def list_schemes(
    category: str | None = Query(default=None, description="Optional category filter"),
    rag_service: RAGService = Depends(get_rag_service),
):
    """List all available government schemes, optionally filtered by category."""
    schemes = rag_service.list_schemes(category=category)
    return schemes


@router.get("/schemes/{scheme_id}", response_model=SchemeDetailSchema)
def get_scheme_by_id(
    scheme_id: str,
    rag_service: RAGService = Depends(get_rag_service),
):
    """Get complete details, eligibility, required documents, and application steps for a specific scheme."""
    scheme = rag_service.get_scheme(scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scheme '{scheme_id}' not found.",
        )
    return scheme


@router.post("/schemes/query", response_model=SchemeQueryResponse)
def query_schemes(
    payload: SchemeQueryRequest,
    db: Session = Depends(get_db),
    rag_service: RAGService = Depends(get_rag_service),
):
    """
    Ask a question about government schemes. Returns a grounded answer with citations
    and official portal references via RAG.
    """
    vendor_context = None
    if payload.vendor_id:
        vendor = db.get(Vendor, payload.vendor_id)
        if vendor:
            vendor_context = {
                "name": vendor.name,
                "product": vendor.product,
                "location": vendor.location,
                "budget": vendor.budget,
                "current_inventory": vendor.current_inventory,
            }

    result = rag_service.answer(payload.query, vendor_context=vendor_context)

    sources = [
        RetrievedChunkSchema(
            source=c.source,
            section=c.section,
            content=c.content,
            score=c.score,
            official_url=c.official_url,
        )
        for c in result.sources
    ]

    matched_schemes = [
        SchemeSummarySchema(
            id=s["id"],
            name=s["name"],
            ministry=s["ministry"],
            category=s["category"],
            max_benefit=s["max_benefit"],
            subsidy_info=s["subsidy_info"],
            collateral_required=s["collateral_required"],
            short_description=s["short_description"],
            official_url=s["official_url"],
        )
        for s in result.matched_schemes
    ]

    return SchemeQueryResponse(
        query=result.query,
        answer=result.answer,
        sources=sources,
        matched_schemes=matched_schemes,
        suggested_followups=result.suggested_followups,
    )


@router.get(
    "/vendors/{vendor_id}/schemes/recommended",
    response_model=VendorRecommendationsResponse,
)
def get_recommended_schemes_for_vendor(
    vendor_id: uuid.UUID,
    db: Session = Depends(get_db),
    rag_service: RAGService = Depends(get_rag_service),
):
    """
    Get personalized government scheme recommendations tailored to a vendor's
    product, budget, location, and inventory constraints.
    """
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found",
        )

    vendor_data = {
        "name": vendor.name,
        "product": vendor.product,
        "location": vendor.location,
        "budget": vendor.budget,
        "current_inventory": vendor.current_inventory,
    }

    recommendations = rag_service.recommend_for_vendor(vendor_data)

    return VendorRecommendationsResponse(
        vendor_id=vendor.id,
        vendor_name=vendor.name,
        recommendations=recommendations,
    )
