"""
FLUX backend entrypoint.

Keeps main.py thin: it only wires together settings, middleware, and
routers. All actual logic lives in app/api, app/services, etc.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api import health, vendors, sales_records

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(vendors.router, prefix=settings.API_V1_PREFIX)
app.include_router(sales_records.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": "FLUX API is running. See /docs for API documentation."}
