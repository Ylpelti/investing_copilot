from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic_core import ValidationError

from app.core.errors.exceptions import DuplicateStockError, NotFound
from app.crud.stock_crud import StockCrud
from app.models import Stock
from app.schemas.stock import StockCreate
from app.services.stocks.stock_service import StockService


@pytest.fixture
def stock_repo(test_db):
    return StockCrud(test_db)


@pytest.fixture
def stock_service(test_db, stock_repo):
    return StockService(stock_repo=stock_repo, db=test_db)


@pytest.fixture
def stock_create_payload():
    return StockCreate(
        ticker="NOKIA.HE",
        isin="FI0009000681",
        name="Nokia Oyj",
        close_price=Decimal("3.45"),
        sector="Technology",
    )


def test_stock_schema_accepts_required_fields(stock_create_payload):
    assert stock_create_payload.ticker == "NOKIA.HE"
    assert stock_create_payload.isin == "FI0009000681"
    assert stock_create_payload.close_price == Decimal("3.45")


def test_stock_schema_requires_isin_and_name():
    with pytest.raises(ValidationError):
        StockCreate(ticker="NOKIA.HE", close_price=Decimal("3.45"))


def test_stock_model_repr_is_readable():
    stock = Stock(
        ticker="NOKIA.HE",
        isin="FI0009000681",
        name="Nokia Oyj",
        close_price=Decimal("3.45"),
        sector="Technology",
    )

    text = repr(stock)

    assert "Stock" in text
    assert "NOKIA.HE" in text
    assert "Nokia Oyj" in text


def test_stock_repo_add_and_lookup(test_db, stock_repo):
    stock = Stock(
        ticker="NOKIA.HE",
        isin="FI0009000681",
        name="Nokia Oyj",
        close_price=Decimal("3.45"),
        sector="Technology",
        updated_at=datetime.now(UTC),
    )

    stock_repo.add(stock)
    test_db.commit()
    test_db.refresh(stock)

    assert stock_repo.get_by_id(stock.id).ticker == "NOKIA.HE"
    assert stock_repo.get_by_ticker("NOKIA.HE").id == stock.id
    assert stock_repo.get_by_isin("FI0009000681").id == stock.id


def test_stock_repo_list_or_search_orders_and_filters(test_db, stock_repo):
    test_db.add_all(
        [
            Stock(ticker="NOKIA.HE", isin="FI0009000681", name="Nokia Oyj", close_price=Decimal("3.45")),
            Stock(ticker="FORTUM.HE", isin="FI0009007132", name="Fortum Oyj", close_price=Decimal("12.50")),
        ]
    )
    test_db.commit()

    all_stocks = stock_repo.list_or_search(q=None, limit=10, offset=0)
    filtered = stock_repo.list_or_search(q="nok", limit=10, offset=0)

    assert [stock.ticker for stock in all_stocks] == ["FORTUM.HE", "NOKIA.HE"]
    assert [stock.ticker for stock in filtered] == ["NOKIA.HE"]


def test_stock_service_creates_stock(stock_service, stock_create_payload):
    created = stock_service.create_stock(stock_create_payload)

    assert created is not None
    assert created.id is not None
    assert created.ticker == "NOKIA.HE"
    assert created.isin == "FI0009000681"


def test_stock_service_duplicate_isin_raises(stock_service, stock_create_payload):
    stock_service.create_stock(stock_create_payload)

    with pytest.raises(DuplicateStockError):
        stock_service.create_stock(stock_create_payload)


def test_stock_service_getters_raise_not_found(stock_service):
    with pytest.raises(NotFound):
        stock_service.get_stock_by_id_or_404(9999)

    with pytest.raises(NotFound):
        stock_service.get_stock_by_ticker("MISSING.HE")

    with pytest.raises(NotFound):
        stock_service.get_stock_by_isin("MISSING-ISIN")


def test_create_stock_api_returns_201(client):
    response = client.post(
        "/api/v1/stocks/",
        json={
            "ticker": "NOKIA.HE",
            "isin": "FI0009000681",
            "name": "Nokia Oyj",
            "close_price": "3.45",
            "sector": "Technology",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["ticker"] == "NOKIA.HE"
    assert body["isin"] == "FI0009000681"


def test_duplicate_stock_api_returns_conflict(client):
    payload = {
        "ticker": "NOKIA.HE",
        "isin": "FI0009000681",
        "name": "Nokia Oyj",
        "close_price": "3.45",
    }

    first = client.post("/api/v1/stocks/", json=payload)
    second = client.post("/api/v1/stocks/", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_stock_read_api_routes(client, test_stock):
    by_id = client.get(f"/api/v1/stocks/{test_stock.id}")
    by_ticker = client.get(f"/api/v1/stocks/by-ticker/{test_stock.ticker}")
    listed = client.get("/api/v1/stocks/?q=fortum&limit=10&offset=0")

    assert by_id.status_code == 200
    assert by_id.json()["ticker"] == test_stock.ticker
    assert by_ticker.status_code == 200
    assert by_ticker.json()["isin"] == test_stock.isin
    assert listed.status_code == 200
    assert listed.json()[0]["ticker"] == test_stock.ticker


def test_missing_stock_api_routes_return_404(client):
    assert client.get("/api/v1/stocks/9999").status_code == 404
    assert client.get("/api/v1/stocks/by-ticker/MISSING.HE").status_code == 404
