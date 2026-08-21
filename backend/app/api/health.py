"""
Health check, readiness/liveness probes, system telemetry, and Prometheus metrics.

Provides standard endpoints for Kubernetes, Docker, and cloud orchestrators:
- GET /api/health          - General service health check (compatible with legacy)
- GET /api/health/live     - Kubernetes liveness probe (checks process is running)
- GET /api/health/ready    - Kubernetes readiness probe (checks DB, ML model, RAG data)
- GET /api/health/detailed - Detailed system telemetry, memory, and runtime metadata
- GET /api/metrics         - Prometheus text format metrics exposition
"""

import os
import platform
import sys
import time
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.metrics import get_metrics_registry
from app.db.session import get_db

router = APIRouter(tags=["health"])

_START_TIME = time.time()


def _check_db(db: Session) -> bool:
    """Executes a lightweight query to verify DB responsiveness."""
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def _check_ml_model() -> Dict[str, Any]:
    """Checks presence and status of the demand forecasting model."""
    try:
        from ml.inference.predict import MODEL_PATH
        if MODEL_PATH.exists():
            return {
                "status": "ready",
                "path": str(MODEL_PATH),
                "model_version": "random_forest_v1",
            }
        return {
            "status": "missing_artifact",
            "message": "Model artifact not found. Needs training or mounting.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def _check_rag_schemes() -> Dict[str, Any]:
    """Checks presence and parsing of the government schemes knowledge base."""
    try:
        from app.services.rag_service import SCHEMES_DATA_PATH, get_rag_service
        if SCHEMES_DATA_PATH.exists():
            rag = get_rag_service()
            schemes = rag.list_schemes()
            return {
                "status": "ready",
                "count": len(schemes),
                "path": str(SCHEMES_DATA_PATH),
            }
        return {
            "status": "missing_data",
            "message": "Schemes data file not found.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """General health check endpoint for backward compatibility."""
    is_db_up = _check_db(db)
    registry = get_metrics_registry()
    registry.set_db_status(is_db_up)

    return {
        "status": "ok" if is_db_up else "degraded",
        "service": "flux-backend",
        "database": "ok" if is_db_up else "unreachable",
    }


@router.get("/health/live")
def liveness_probe():
    """
    Kubernetes Liveness Probe.
    Returns 200 OK as long as the FastAPI process is responsive.
    """
    return {
        "status": "alive",
        "uptime_seconds": round(time.time() - _START_TIME, 2),
    }


@router.get("/health/ready")
def readiness_probe(db: Session = Depends(get_db)):
    """
    Kubernetes Readiness Probe.
    Verifies that the database is reachable, ML model is available, and RAG data is loaded.
    Returns 503 Service Unavailable if any critical component is failing.
    """
    db_ok = _check_db(db)
    ml_status = _check_ml_model()
    rag_status = _check_rag_schemes()

    registry = get_metrics_registry()
    registry.set_db_status(db_ok)

    is_ready = db_ok and ml_status.get("status") == "ready" and rag_status.get("status") == "ready"

    payload = {
        "status": "ready" if is_ready else "not_ready",
        "checks": {
            "database": "connected" if db_ok else "unreachable",
            "ml_model": ml_status,
            "rag_knowledge_base": rag_status,
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    if not is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=payload,
        )

    return payload


@router.get("/health/detailed")
def detailed_health(db: Session = Depends(get_db)):
    """
    Comprehensive system telemetry, diagnostics, and component status.
    """
    db_ok = _check_db(db)
    ml_status = _check_ml_model()
    rag_status = _check_rag_schemes()
    registry = get_metrics_registry()
    registry.set_db_status(db_ok)

    # Process memory stats if available
    mem_info = {}
    try:
        import resource  # Available on Unix/Linux
        mem_info["max_rss_kb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except (ImportError, AttributeError):
        pass

    return {
        "status": "ok" if db_ok else "degraded",
        "service": {
            "name": "FLUX Production Backend",
            "version": "1.0.0",
            "environment": os.getenv("APP_ENV", "production"),
            "uptime_seconds": round(time.time() - _START_TIME, 2),
        },
        "system": {
            "platform": platform.platform(),
            "python_version": sys.version.split()[0],
            "cpu_count": os.cpu_count() or 1,
            "pid": os.getpid(),
            "memory": mem_info,
        },
        "components": {
            "database": {
                "status": "connected" if db_ok else "unreachable",
                "engine": "PostgreSQL 16 (SQLAlchemy ORM)",
            },
            "ml_forecast_engine": ml_status,
            "rag_scheme_advisor": rag_status,
            "metrics_registry": {
                "in_flight_requests": registry.in_flight_requests,
                "recorded_endpoints": len(registry.http_request_durations),
            },
        },
    }


@router.get("/metrics", response_class=Response)
def prometheus_metrics():
    """
    Prometheus metrics scraper exposition endpoint.
    Returns metrics in Prometheus text format 0.0.4.
    """
    registry = get_metrics_registry()
    text_content = registry.generate_prometheus_text()
    return Response(
        content=text_content,
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
