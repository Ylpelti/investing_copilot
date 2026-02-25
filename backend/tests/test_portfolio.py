import pytest

from app.core.errors.exceptions import Forbidden, NotFound
from app.crud.portfolio_crud import PortfolioCrud
from app.crud.position_crud import PositionCrud
from app.models import Portfolio, User
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.services.portfolio.portfolio_service import PortfolioService


@pytest.fixture
def portfolio_service(test_db, test_user):
    return PortfolioService(
        db=test_db,
        current_user_id=test_user.id,
        portfolio_repo=PortfolioCrud(test_db),
        position_repo=PositionCrud(test_db),
    )


def test_create_portfolio_service(portfolio_service, test_user):
    created = portfolio_service.create_portfolio(
        PortfolioCreate(name="Test Portfolio", description="desc")
    )
    assert created.id is not None
    assert created.user_id == test_user.id
    assert created.name == "Test Portfolio"


def test_create_portfolio_default_name(portfolio_service):
    created = portfolio_service.create_portfolio(PortfolioCreate(description=None))
    assert created.id is not None
    assert created.name == "Untitled Portfolio"


def test_get_owned_portfolio_or_404_missing(portfolio_service):
    with pytest.raises(NotFound):
        portfolio_service.get_owned_portfolio_or_404(9999)


def test_get_owned_portfolio_or_404_forbidden(test_db, portfolio_service, test_user):
    other_user = User(username="otheruser", email="other@example.com", pw_hash="hash")
    test_db.add(other_user)
    test_db.commit()
    test_db.refresh(other_user)

    foreign = Portfolio(name="Foreign", user_id=other_user.id, description=None)
    test_db.add(foreign)
    test_db.commit()
    test_db.refresh(foreign)

    with pytest.raises(Forbidden):
        portfolio_service.get_owned_portfolio_or_404(foreign.id)


def test_update_portfolio_service(portfolio_service):
    created = portfolio_service.create_portfolio(
        PortfolioCreate(name="Original", description="old")
    )
    updated = portfolio_service.update_portfolio(
        PortfolioUpdate(name="Updated", description="new"),
        created.id,
    )
    assert updated.name == "Updated"
    assert updated.description == "new"


def test_delete_portfolio_service(portfolio_service, test_db):
    created = portfolio_service.create_portfolio(
        PortfolioCreate(name="Delete me", description=None)
    )
    portfolio_service.delete_portfolio(created.id)
    deleted = test_db.get(Portfolio, created.id)
    assert deleted is None


def test_create_portfolio_api(client, auth_headers):
    response = client.post(
        "/api/v1/portfolios/",
        headers=auth_headers,
        json={"name": "API Portfolio", "description": "via api"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "API Portfolio"
    assert body["description"] == "via api"
    assert "id" in body


def test_list_my_portfolios_api(client, auth_headers):
    client.post(
        "/api/v1/portfolios/",
        headers=auth_headers,
        json={"name": "P1", "description": None},
    )
    response = client.get("/api/v1/portfolios/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_get_update_delete_portfolio_api(client, auth_headers):
    created = client.post(
        "/api/v1/portfolios/",
        headers=auth_headers,
        json={"name": "To edit", "description": "before"},
    ).json()

    portfolio_id = created["id"]
    fetched = client.get(f"/api/v1/portfolios/{portfolio_id}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["id"] == portfolio_id

    updated = client.put(
        f"/api/v1/portfolios/{portfolio_id}",
        headers=auth_headers,
        json={"description": "after"},
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "after"

    deleted = client.delete(f"/api/v1/portfolios/{portfolio_id}", headers=auth_headers)
    assert deleted.status_code == 204
