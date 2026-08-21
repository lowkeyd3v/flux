"""
Tests for production health probes, readiness/liveness, Prometheus metrics, and tracing.
"""

from fastapi.testclient import TestClient


def test_liveness_probe_returns_200(client: TestClient):
    response = client.get("/api/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "uptime_seconds" in data
    assert data["uptime_seconds"] >= 0


def test_readiness_probe_returns_200_when_ready(client: TestClient):
    response = client.get("/api/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "checks" in data
    assert data["checks"]["database"] == "connected"
    assert data["checks"]["ml_model"]["status"] == "ready"
    assert data["checks"]["rag_knowledge_base"]["status"] == "ready"


def test_detailed_health_telemetry(client: TestClient):
    response = client.get("/api/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "system" in data
    assert "components" in data
    assert data["components"]["database"]["status"] == "connected"
    assert data["components"]["ml_forecast_engine"]["status"] == "ready"
    assert data["components"]["rag_scheme_advisor"]["status"] == "ready"


def test_prometheus_metrics_endpoint(client: TestClient):
    # Perform some requests first to populate counters
    client.get("/api/health")
    client.get("/api/schemes")

    response = client.get("/api/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    
    content = response.text
    assert "flux_app_uptime_seconds" in content
    assert "flux_db_status" in content
    assert "flux_http_requests_total" in content
    assert "flux_http_request_duration_seconds" in content


def test_root_metrics_endpoint_alias(client: TestClient):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "flux_app_uptime_seconds" in response.text


def test_request_id_tracing_header_generation(client: TestClient):
    # When no X-Request-ID is sent, backend generates one
    response = client.get("/api/health")
    assert response.status_code == 200
    req_id = response.headers.get("X-Request-ID")
    assert req_id is not None
    assert len(req_id) > 10


def test_request_id_tracing_header_propagation(client: TestClient):
    # When X-Request-ID is provided by caller, backend preserves it
    custom_id = "test-custom-trace-uuid-12345"
    response = client.get("/api/health", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_id
