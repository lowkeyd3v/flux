"""
Gunicorn configuration for FLUX FastAPI production deployment.
"""

import multiprocessing
import os

# Server socket
bind = os.getenv("BIND", "0.0.0.0:8000")
backlog = 2048

# Worker processes
# Calculate workers: default to (2 x $num_cores) + 1, capped between 2 and 8
calculated_workers = min(max((multiprocessing.cpu_count() * 2) + 1, 2), 8)
workers = int(os.getenv("WEB_CONCURRENCY", calculated_workers))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = int(os.getenv("TIMEOUT", 60))
keepalive = int(os.getenv("KEEP_ALIVE", 5))
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", 30))

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" (%(L)ss)'

# Process naming
proc_name = "flux-fastapi-backend"
