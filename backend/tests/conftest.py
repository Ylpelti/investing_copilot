import pytest
from app import models
from app.db.session import SessionLocal, Base, engine
from app.security.hashing import hash_password
from datetime import datetime, UTC
from app.schemas.stock import StockCreate


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(test_db):
    user = models.User(username="testuser", email="testuser@example.com", pw_hash="salainen123")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

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
        ticker="FORTUM",
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