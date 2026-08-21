# FLUX Monitoring & Observability Guide

This guide details the observability architecture, metrics collection, structured JSON logging, distributed request tracing, and alerting thresholds for FLUX.

---

## 1. Observability Architecture

```
+-----------------------------------------------------------------------------------+
|                               FLUX FastAPI Backend                                |
|                                                                                   |
|  [ RequestTracingMiddleware ]  --> Generates/Propagates X-Request-ID Header       |
|  [ StructuredLoggingMiddleware ] --> Emits JSON Access Logs to stdout            |
|  [ MetricsMiddleware ]          --> Collects Request Counts, Latencies, In-flight  |
|  [ ML & RAG Timers ]            --> Tracks Model Inference & Vector Search Times  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
                         +-------------------------------+
                         |   GET /api/metrics (PromQL)   |
                         +-------------------------------+
                                         |
                                         v (Scraped every 15s)
                         +-------------------------------+
                         |   Prometheus Time-Series DB   |
                         +-------------------------------+
                                         |
                                         v
                         +-------------------------------+
                         |   Grafana Real-Time Dashboard |
                         +-------------------------------+
```

---

## 2. Key Metrics Reference

| Metric Name | Type | Description | Labels |
|---|---|---|---|
| `flux_app_uptime_seconds` | Gauge | Total uptime of the API service in seconds | - |
| `flux_db_status` | Gauge | Database connectivity indicator (1=UP, 0=DOWN) | - |
| `flux_http_requests_in_flight` | Gauge | Active requests currently being processed | - |
| `flux_http_requests_total` | Counter | Cumulative HTTP requests served | `method`, `endpoint`, `status` |
| `flux_http_request_duration_seconds` | Summary | Request latency distribution in seconds | `endpoint`, `quantile` (`0.5`, `0.9`, `0.99`) |
| `flux_ml_prediction_duration_seconds` | Summary | Random Forest demand model inference time | `quantile` (`0.5`, `0.95`) |
| `flux_rag_query_duration_seconds` | Summary | Government scheme RAG retrieval & answer latency | `quantile` (`0.5`, `0.95`) |

---

## 3. Standard Health Probes

| Probe Endpoint | Purpose | Target Orchestrator | Expected Response |
|---|---|---|---|
| `GET /api/health` | Service & DB connectivity check | Legacy clients / Docker Compose | `{"status": "ok", "database": "ok"}` |
| `GET /api/health/live` | Process responsiveness probe | Kubernetes Liveness Probe | `200 OK` with `uptime_seconds` |
| `GET /api/health/ready` | Deep dependency check (DB + ML + RAG) | Kubernetes Readiness Probe | `200 OK` (or `503` if DB unreachable) |
| `GET /api/health/detailed` | Diagnostics, CPU, memory, models | Operations & DevOps telemetry | `200 OK` with full component status |

---

## 4. Structured JSON Logging Format

Every HTTP transaction generates a single structured JSON line written to `stdout`:

```json
{
  "timestamp": "2026-08-21T18:14:31Z",
  "request_id": "206737a2-c1e0-48a8-bb50-513bb37969a2",
  "method": "POST",
  "path": "/api/vendors/8f3b14ac-1234/predict",
  "status_code": 200,
  "duration_ms": 14.28,
  "client_ip": "192.168.1.50",
  "user_agent": "Mozilla/5.0 (Linux; Android 14) Chrome/120.0"
}
```

---

## 5. Recommended Alert Rules (Prometheus Alertmanager)

```yaml
groups:
  - name: flux-production-alerts
    rules:
      - alert: DatabaseDown
        expr: flux_db_status == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "FLUX PostgreSQL Database is Unreachable"

      - alert: HighErrorRate
        expr: sum(rate(flux_http_requests_total{status=~"5.."}[5m])) / sum(rate(flux_http_requests_total[5m])) > 0.05
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "FLUX API 5xx error rate exceeds 5%"

      - alert: HighMLInferenceLatency
        expr: flux_ml_prediction_duration_seconds{quantile="0.95"} > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "95th percentile ML prediction latency is over 500ms"
```
