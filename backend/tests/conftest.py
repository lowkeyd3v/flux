"""
Shared pytest fixtures.

Uses the PostgreSQL database configured via DATABASE_URL, ensures all schema tables
are created, verifies ML model artifacts, and wraps each test in a transaction.
"""

import sys
from pathlib import Path

# Ensure backend and repo root are in sys.path
_BACKEND_DIR = Path(__file__).resolve().parents[1]
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import engine, get_db, Base
from app.models import Vendor, SalesRecord  # noqa: F401 - ensure models are registered


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Ensure database schema tables and ML model artifact are ready for tests."""
    Base.metadata.create_all(bind=engine)

    from ml.inference.predict import MODEL_PATH
    if not MODEL_PATH.exists():
        from ml.data.generate_synthetic_data import generate_synthetic_dataset, OUTPUT_PATH
        from ml.training.train_demand_model import train
        df = generate_synthetic_dataset()
        df.to_csv(OUTPUT_PATH, index=False)
        train()
    yield


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
