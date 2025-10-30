import pytest
from app import models
from app.db.session import SessionLocal, Base, engine
from app.security.hashing import hash_password
from datetime import datetime

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
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
    portfolio = models.Portfolio(name="Test portfolio", user_id=test_user.id)
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
        updated_at=datetime.utcnow(),
    )
    test_db.add(stock)
    test_db.commit()
    test_db.refresh(stock)
    return stock