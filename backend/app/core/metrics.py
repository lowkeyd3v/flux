"""
Prometheus metrics collector and exporter for the FLUX FastAPI backend.

Provides in-memory thread-safe metric counters, histograms, and gauges
formatted to standard Prometheus text exposition format (version 0.0.4),
without requiring heavy external C-extensions.
"""

import threading
import time
from collections import defaultdict
from typing import Dict, List, Tuple


class MetricsRegistry:
    """Thread-safe Prometheus metrics store for FLUX."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        
        # HTTP request counts: (method, endpoint, status_code) -> count
        self.http_requests_total: Dict[Tuple[str, str, int], int] = defaultdict(int)
        
        # HTTP request durations: list of elapsed seconds per endpoint
        self.http_request_durations: Dict[str, List[float]] = defaultdict(list)
        
        # ML inference durations: list of elapsed seconds
        self.ml_prediction_durations: List[float] = []
        
        # RAG query durations: list of elapsed seconds
        self.rag_query_durations: List[float] = []
        
        # In-flight active requests
        self.in_flight_requests: int = 0
        
        # Service start time
        self.start_time: float = time.time()
        
        # Database connectivity gauge (1 = UP, 0 = DOWN)
        self.db_status: int = 1

    def record_request_start(self) -> None:
        with self._lock:
            self.in_flight_requests += 1

    def record_request_end(
        self, method: str, endpoint: str, status_code: int, duration_seconds: float
    ) -> None:
        with self._lock:
            if self.in_flight_requests > 0:
                self.in_flight_requests -= 1
            self.http_requests_total[(method, endpoint, status_code)] += 1
            # Keep last 1000 durations to prevent unbounded memory growth
            durations = self.http_request_durations[endpoint]
            durations.append(duration_seconds)
            if len(durations) > 1000:
                self.http_request_durations[endpoint] = durations[-1000:]

    def record_ml_prediction(self, duration_seconds: float) -> None:
        with self._lock:
            self.ml_prediction_durations.append(duration_seconds)
            if len(self.ml_prediction_durations) > 500:
                self.ml_prediction_durations = self.ml_prediction_durations[-500:]

    def record_rag_query(self, duration_seconds: float) -> None:
        with self._lock:
            self.rag_query_durations.append(duration_seconds)
            if len(self.rag_query_durations) > 500:
                self.rag_query_durations = self.rag_query_durations[-500:]

    def set_db_status(self, is_up: bool) -> None:
        with self._lock:
            self.db_status = 1 if is_up else 0

    def generate_prometheus_text(self) -> str:
        """Generates valid Prometheus text exposition output."""
        lines = []
        
        # Header
        lines.append("# HELP flux_app_uptime_seconds Total seconds since FLUX API started")
        lines.append("# TYPE flux_app_uptime_seconds gauge")
        uptime = time.time() - self.start_time
        lines.append(f"flux_app_uptime_seconds {uptime:.2f}")
        
        lines.append("# HELP flux_db_status PostgreSQL database connection status (1=UP, 0=DOWN)")
        lines.append("# TYPE flux_db_status gauge")
        lines.append(f"flux_db_status {self.db_status}")
        
        lines.append("# HELP flux_http_requests_in_flight Current in-flight active HTTP requests")
        lines.append("# TYPE flux_http_requests_in_flight gauge")
        lines.append(f"flux_http_requests_in_flight {self.in_flight_requests}")
        
        # Total requests counter
        lines.append("# HELP flux_http_requests_total Total number of HTTP requests processed")
        lines.append("# TYPE flux_http_requests_total counter")
        with self._lock:
            for (method, endpoint, status_code), count in sorted(self.http_requests_total.items()):
                lines.append(
                    f'flux_http_requests_total{{method="{method}",endpoint="{endpoint}",status="{status_code}"}} {count}'
                )
            
            # Latency summary / percentiles
            lines.append("# HELP flux_http_request_duration_seconds HTTP request latency summary in seconds")
            lines.append("# TYPE flux_http_request_duration_seconds summary")
            for endpoint, durations in sorted(self.http_request_durations.items()):
                if not durations:
                    continue
                sorted_d = sorted(durations)
                total = sum(sorted_d)
                count = len(sorted_d)
                p50 = sorted_d[int(count * 0.50)]
                p90 = sorted_d[int(count * 0.90)]
                p99 = sorted_d[min(int(count * 0.99), count - 1)]
                lines.append(f'flux_http_request_duration_seconds{{endpoint="{endpoint}",quantile="0.5"}} {p50:.6f}')
                lines.append(f'flux_http_request_duration_seconds{{endpoint="{endpoint}",quantile="0.9"}} {p90:.6f}')
                lines.append(f'flux_http_request_duration_seconds{{endpoint="{endpoint}",quantile="0.99"}} {p99:.6f}')
                lines.append(f'flux_http_request_duration_seconds_sum{{endpoint="{endpoint}"}} {total:.6f}')
                lines.append(f'flux_http_request_duration_seconds_count{{endpoint="{endpoint}"}} {count}')

            # ML prediction durations
            lines.append("# HELP flux_ml_prediction_duration_seconds Random Forest inference latency in seconds")
            lines.append("# TYPE flux_ml_prediction_duration_seconds summary")
            if self.ml_prediction_durations:
                sorted_ml = sorted(self.ml_prediction_durations)
                lines.append(f'flux_ml_prediction_duration_seconds{{quantile="0.5"}} {sorted_ml[int(len(sorted_ml)*0.5)]:.6f}')
                lines.append(f'flux_ml_prediction_duration_seconds{{quantile="0.95"}} {sorted_ml[min(int(len(sorted_ml)*0.95), len(sorted_ml)-1)]:.6f}')
                lines.append(f'flux_ml_prediction_duration_seconds_sum {sum(sorted_ml):.6f}')
                lines.append(f'flux_ml_prediction_duration_seconds_count {len(sorted_ml)}')
            else:
                lines.append("flux_ml_prediction_duration_seconds_count 0")

            # RAG query durations
            lines.append("# HELP flux_rag_query_duration_seconds Government scheme RAG retrieval and synthesis latency in seconds")
            lines.append("# TYPE flux_rag_query_duration_seconds summary")
            if self.rag_query_durations:
                sorted_rag = sorted(self.rag_query_durations)
                lines.append(f'flux_rag_query_duration_seconds{{quantile="0.5"}} {sorted_rag[int(len(sorted_rag)*0.5)]:.6f}')
                lines.append(f'flux_rag_query_duration_seconds{{quantile="0.95"}} {sorted_rag[min(int(len(sorted_rag)*0.95), len(sorted_rag)-1)]:.6f}')
                lines.append(f'flux_rag_query_duration_seconds_sum {sum(sorted_rag):.6f}')
                lines.append(f'flux_rag_query_duration_seconds_count {len(sorted_rag)}')
            else:
                lines.append("flux_rag_query_duration_seconds_count 0")

        lines.append("")  # End with newline
        return "\n".join(lines)


# Singleton registry instance
metrics_registry = MetricsRegistry()


def get_metrics_registry() -> MetricsRegistry:
    """Returns the shared application metrics registry instance."""
    return metrics_registry
