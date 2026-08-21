# ==============================================================================
# FLUX Production Backend Dockerfile
# Multi-stage build for lightweight, secure FastAPI + Scikit-Learn ML inference
# ==============================================================================

# --- Stage 1: Build & Dependencies ---
FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn==23.0.0

# --- Stage 2: Final Runtime Image ---
FROM python:3.11-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:/app/backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy globally installed Python packages and entrypoint binaries from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root system user
RUN groupadd -g 10001 fluxgroup && \
    useradd -u 10001 -g fluxgroup -s /bin/bash -m fluxuser

# Copy application files
COPY backend /app/backend
COPY ml /app/ml

# Copy entrypoint and config to root of /app
COPY backend/docker-entrypoint.sh /app/docker-entrypoint.sh
COPY backend/gunicorn_conf.py /app/gunicorn_conf.py

# Generate synthetic data & train ML model artifact during build
RUN python -m ml.data.generate_synthetic_data && \
    python -m ml.training.train_demand_model

# Fix permissions
RUN chmod +x /app/docker-entrypoint.sh && \
    chown -R fluxuser:fluxgroup /app

# Switch to unprivileged user
USER fluxuser

EXPOSE 8000

# Native healthcheck
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]
