import io
import pytest
from app.core.errors.exceptions import NotFound, Forbidden, BadRequest
import pandas as pd
from app.services.portfolio_import_service import parse_csv
from app.models.positio import Position
from app.crud.portfolio_crud import PortfolioCrud
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.schemas.user import UserCreate
from app.models import User, Portfolio



@pytest.fixture
def test_crud(test_db):
    return PortfolioCrud(test_db)

def test_create_portfolio(test_crud, test_user):
    fake_portfolio = PortfolioCreate(name="Test Portfolio", description="desc", user_id=test_user.id)
    result = test_crud.create_portfolio(fake_portfolio)

    assert result.id is not None
    assert result.name == "Test Portfolio"
    assert result.user_id == 1

def test_create_portfolio_without_description(test_crud, test_user):
    fake_portfolio = PortfolioCreate(name="Test Portfolio", description=None, user_id=test_user.id)
    result = test_crud.create_portfolio(fake_portfolio)

    assert result.id is not None
    assert result.description is None

def test_creating_portfolio_with_default_name(test_crud, test_user):
    fake_portfolio = PortfolioCreate( description=None, user_id=test_user.id)
    result = test_crud.create_portfolio(fake_portfolio)

    assert result.id is not None
    assert result.name == "Untitled Portfolio"

def test_read_owned_portfolio(test_crud, test_user):
    fake_portfolio = PortfolioCreate(name="Test Portfolio", description="desc", user_id=test_user.id)
    created_portfolio = test_crud.create_portfolio(fake_portfolio)
    fetched_portfolio = test_crud.get_owned_portfolio(created_portfolio.id, test_user.id)

    assert fetched_portfolio.id == created_portfolio.id
    assert fetched_portfolio.user_id == test_user.id
    assert fetched_portfolio.name == "Test Portfolio"

def test_read_non_existing_portfolio(test_crud):
    with pytest.raises(NotFound) as exc_info:
        test_crud.get_owned_portfolio(5, 8)

    assert "not found" in exc_info.value.message.lower()
    assert exc_info.value.status_code == 404

def test_not_owned_portfolio(test_crud, test_user, test_db):
    other_user = User(username="otheruser", email="other@example.com", pw_hash="pass")
    test_db.add(other_user)
    test_db.commit()
    test_db.refresh(other_user)

    portfolio = Portfolio(name="Other's Portfolio", user_id=other_user.id)
    test_db.add(portfolio)
    test_db.commit()
    test_db.refresh(portfolio)

    with pytest.raises(Forbidden) as exc_info:
        test_crud.get_owned_portfolio(portfolio.id, test_user.id)

    assert exc_info.value.status_code == 403

def test_invalid_user_id(test_crud, test_user, test_db):
    portfolio = Portfolio(name="Other's Portfolio", user_id=test_user.id)
    test_db.add(portfolio)
    test_db.commit()
    test_db.refresh(portfolio)
    with pytest.raises(Forbidden) as exc_info:
        test_crud.get_owned_portfolio(portfolio.id, 100)
    assert exc_info.value.status_code == 403

def test_updating_portfolio_both_fields(test_crud, test_user, test_db):
    portfolio = Portfolio(name="Other's Portfolio", user_id=test_user.id)
    test_db.add(portfolio)
    test_db.commit()
    test_db.refresh(portfolio)

    updated_portfolio = PortfolioUpdate(name="Updated portfolio", description="This portfolio have been updated")

    result = test_crud.update_portfolio(portfolio.id, updated_portfolio, test_user.id)

    assert result.name == "Updated portfolio"
    assert result.id == portfolio.id
    assert result.description == "This portfolio have been updated"

def test_updating_only_one_field(test_crud, test_user, test_db):
    portfolio = Portfolio(name="Test Portfolio", user_id=test_user.id)
    test_db.add(portfolio)
    test_db.commit()
    test_db.refresh(portfolio)

    updated_portfolio = PortfolioUpdate(description="This portfolio have been updated")

    result = test_crud.update_portfolio(portfolio.id, updated_portfolio, test_user.id)

    assert result.name == "Test Portfolio"
    assert result.id == portfolio.id
    assert result.description == "This portfolio have been updated"

def test_deleting_portfolio(test_crud, test_user, test_db):
    portfolio = Portfolio(name="Test Portfolio", user_id=test_user.id)
    test_db.add(portfolio)
    test_db.commit()
    test_db.refresh(portfolio)

    result = test_crud.delete_portfolio(portfolio.id, test_user.id)

    assert result == True

    deleted = test_db.get(Portfolio, portfolio.id)
    assert deleted is None




    



    



    







def test_portfolio_import(test_db, test_portfolio, test_stock):

    csv_data = """Tulostuspäivä\tSalkku\tHankintapäivä\tInstrumentti\tTunnus\tISIN\tValuutta\tMäärä\tHankinta-arvo (Noteerausvaluutta)\tHankintahinta (EUR)
    7.10.2025\t19568203\t3.4.2024\tFortum\tFORTUM\tFI0009007132\tEUR\t10\t12.5\t125,0
    """

    fake_file = io.StringIO(csv_data)

    parse_csv(fake_file, portfolio_id=test_portfolio.id, db=test_db)

    positions = test_db.query(Position).all()
    assert len(positions) == 1
    assert positions[0].quantity == 10
    assert positions[0].buy_price == 12.5
    assert len(positions) != 2






    