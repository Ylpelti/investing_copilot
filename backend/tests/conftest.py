from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.api.v1.api import api_router
from app.core.errors.errorhandler import app_error_handler, generic_exception_handler
from app.core.errors.exceptions import AppError
from app.db.base_class import Base
from app.db.session import get_db
from app.schemas.stock import StockCreate
from app.security.auth import create_access_token
from app.security.hashing import hash_password

# Ensure metadata includes all models.
import app.db.base  # noqa: F401,E402


TEST_ENGINE = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=TEST_ENGINE)
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture(scope="function")
def app(test_db):
    app = FastAPI(debug=True)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    app.include_router(api_router, prefix="/api/v1")

    def _get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = _get_test_db
    try:
        yield app
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(test_db):
    user = models.User(
        username="testuser",
        email="testuser@example.com",
        pw_hash=hash_password("salainen123"),
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token({"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_portfolio(test_db, test_user):
    portfolio = models.Portfolio(name="Test portfolio", user_id=test_user.id, description=None)
    test_db.add(portfolio)
    test_db.commit()
    test_db.refresh(portfolio)
    return portfolio


@pytest.fixture
def test_stock(test_db):
    stock = models.Stock(
        ticker="FORTUM.HE",
        isin="FI0009007132",
        name="Fortum Oyj",
        close_price=12.45,
        sector="Energy",
        updated_at=datetime.now(UTC),
    )
    test_db.add(stock)
    test_db.commit()
    test_db.refresh(stock)
    return stock


@pytest.fixture
def fake_stock_data():
    return StockCreate(
        ticker="NOKIA.HE",
        name="Nokia Oyj",
        isin="FI0009000681",
        close_price=3.45,
        sector="Technology",
        updated_at=datetime.now(UTC),
    )
