#!/usr/bin/env bash
set -e

echo "=== [FLUX Backend] Starting container initialization ==="

# Wait for PostgreSQL database readiness
echo "--> Checking database connectivity..."
python3 - <<'EOF'
import os
import sys
import time
import psycopg2

db_url = os.getenv("DATABASE_URL", "postgresql://flux_user:flux_password@postgres:5432/flux_db")

# Normalize SQLAlchemy connection string prefix for psycopg2 driver
if db_url.startswith("postgresql+psycopg2://"):
    db_url = db_url.replace("postgresql+psycopg2://", "postgresql://", 1)

max_retries = 30
retry_interval = 2

for attempt in range(1, max_retries + 1):
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print(f"--> Database is ready! (Connected on attempt {attempt})")
        sys.exit(0)
    except Exception as e:
        print(f"--> Database not ready yet ({e}). Retrying ({attempt}/{max_retries})...")
        time.sleep(retry_interval)

print("--> ERROR: Timed out waiting for database connection.")
sys.exit(1)
EOF

# Run database migrations
echo "--> Running Alembic database migrations (alembic upgrade head)..."
cd /app/backend
alembic upgrade head
echo "--> Database migrations completed successfully."

# Start Gunicorn / Uvicorn ASGI Server
echo "--> Launching Gunicorn ASGI production server..."
cd /app/backend
exec gunicorn -c /app/gunicorn_conf.py app.main:app
