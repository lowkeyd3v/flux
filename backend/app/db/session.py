"""
Database engine and session management.

Provides a `get_db` FastAPI dependency that yields a SQLAlchemy session
per-request and ensures it's closed afterward.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
