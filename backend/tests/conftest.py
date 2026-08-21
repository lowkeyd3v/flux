"""
Shared pytest fixtures.

Uses the same PostgreSQL database configured via DATABASE_URL, but wraps
each test in a transaction that's rolled back afterward, so tests don't
leave leftover data behind or depend on execution order.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import engine, get_db
from app.db.session import Base
from app.models import Vendor, SalesRecord  # noqa: F401 - ensure models are registered


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
