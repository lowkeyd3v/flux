"""
FLUX production backend entrypoint.

Wires together settings, tracing/metrics middleware, CORS, and REST route controllers.
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.middleware import RequestTracingMiddleware, MetricsAndLoggingMiddleware
from app.core.metrics import get_metrics_registry
from app.api import (
    health,
    vendors,
    sales_records,
    predictions,
    recommendations,
    schemes,
    voice,
)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# 1. Tracing & Logging / Metrics Middlewares
app.add_middleware(MetricsAndLoggingMiddleware)
app.add_middleware(RequestTracingMiddleware)

# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount Routers under API prefix (e.g. /api)
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(vendors.router, prefix=settings.API_V1_PREFIX)
app.include_router(sales_records.router, prefix=settings.API_V1_PREFIX)
app.include_router(predictions.router, prefix=settings.API_V1_PREFIX)
app.include_router(recommendations.router, prefix=settings.API_V1_PREFIX)
app.include_router(schemes.router, prefix=settings.API_V1_PREFIX)
app.include_router(voice.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    """Root landing endpoint with system status overview."""
    return {
        "message": "FLUX API is running. See /docs for API documentation.",
        "name": "FLUX Production API",
        "status": "online",
        "environment": settings.APP_ENV,
        "documentation": "/docs",
        "health_check": f"{settings.API_V1_PREFIX}/health",
        "readiness_probe": f"{settings.API_V1_PREFIX}/health/ready",
        "liveness_probe": f"{settings.API_V1_PREFIX}/health/live",
        "metrics": f"{settings.API_V1_PREFIX}/metrics",
    }


@app.get("/metrics", response_class=Response, include_in_schema=False)
def root_metrics():
    """Exposes /metrics at root level as well as /api/metrics for standard Prometheus scrapers."""
    registry = get_metrics_registry()
    return Response(
        content=registry.generate_prometheus_text(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
