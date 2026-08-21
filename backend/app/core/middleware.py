"""
Production ASGI middlewares for request tracing, structured logging, and metrics.
"""

import json
import logging
import re
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.metrics import get_metrics_registry

logger = logging.getLogger("flux.access")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

# Regex to normalize UUIDs and integers in route paths for aggregated metric grouping
UUID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
NUMERIC_PATTERN = re.compile(r"/\d+(?=/|$)")


def normalize_path(path: str) -> str:
    """Replaces dynamic IDs (UUIDs, integers) in path with parameterized placeholders for Prometheus grouping."""
    p = UUID_PATTERN.sub("{id}", path)
    p = NUMERIC_PATTERN.sub("/{id}", p)
    return p


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """
    Ensures every HTTP request has an X-Request-ID for distributed tracing.
    If the caller provided one (e.g. from an upstream CDN or gateway), preserves it;
    otherwise generates a new UUIDv4.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())

        # Store in request state for access in endpoints / subsequent middleware
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class MetricsAndLoggingMiddleware(BaseHTTPMiddleware):
    """
    Combined high-efficiency middleware that:
    1. Tracks Prometheus request metrics (durations, status counts, in-flight gauges).
    2. Emits structured JSON access logs with request IDs, response times, and status.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        registry = get_metrics_registry()
        registry.record_request_start()
        
        start_time = time.time()
        path = request.url.path
        method = request.method
        normalized_path = normalize_path(path)
        request_id = getattr(request.state, "request_id", request.headers.get("X-Request-ID", "-"))
        client_ip = request.client.host if request.client else "unknown"

        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            elapsed_seconds = time.time() - start_time
            elapsed_ms = round(elapsed_seconds * 1000, 2)
            
            # Record Prometheus metrics
            registry.record_request_end(
                method=method,
                endpoint=normalized_path,
                status_code=status_code,
                duration_seconds=elapsed_seconds,
            )

            # Avoid spamming access logs on Prometheus scrape if high frequency, but log all standard requests
            log_payload = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "request_id": request_id,
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": elapsed_ms,
                "client_ip": client_ip,
                "user_agent": request.headers.get("user-agent", "unknown"),
            }
            logger.info(json.dumps(log_payload))
