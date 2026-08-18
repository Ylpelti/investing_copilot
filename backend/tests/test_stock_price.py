from datetime import date
from decimal import Decimal

import pytest

from app.core.errors.exceptions import BadRequest, NotFound
from app.crud.stock_crud import StockCrud
from app.crud.stock_prices_crud import StockPriceCrud
from app.dto.stock_price_dto import ExternalStockPriceDTO
from app.models import Stock, StockPrice
from app.services.stocks.stock_price_service import StockPriceService


@pytest.fixture
def sample_stock(test_db):
    stock = Stock(
        ticker="NOKIA.HE",
        isin="FI0009000681",
        name="Nokia Oyj",
        close_price=Decimal("3.45"),
        sector="Technology",
    )
    test_db.add(stock)
    test_db.commit()
    test_db.refresh(stock)
    return stock


@pytest.fixture
def sample_prices(test_db, sample_stock):
    prices = [
        StockPrice(
            stock_id=sample_stock.id,
            date=date(2025, 11, 1),
            open_price=Decimal("3.40"),
            high_price=Decimal("3.50"),
            low_price=Decimal("3.35"),
            close_price=Decimal("3.45"),
            volume=100000,
        ),
        StockPrice(
            stock_id=sample_stock.id,
            date=date(2025, 11, 2),
            open_price=Decimal("3.45"),
            high_price=Decimal("3.55"),
            low_price=Decimal("3.40"),
            close_price=Decimal("3.50"),
            volume=120000,
        ),
    ]
    test_db.add_all(prices)
    test_db.commit()
    return prices


@pytest.fixture
def price_repo(test_db):
    return StockPriceCrud(test_db)


@pytest.fixture
def price_service(test_db):
    return StockPriceService(StockCrud(test_db), StockPriceCrud(test_db))


def test_stock_price_repo_get_prices_filters_and_orders(price_repo, sample_stock, sample_prices):
    results = price_repo.get_prices(
        stock_id=sample_stock.id,
        start_date=date(2025, 11, 1),
        end_date=date(2025, 11, 2),
        limit=10,
        order="asc",
    )

    assert [price.date for price in results] == [date(2025, 11, 1), date(2025, 11, 2)]


def test_stock_price_repo_get_prices_desc_limit(price_repo, sample_stock, sample_prices):
    results = price_repo.get_prices(
        stock_id=sample_stock.id,
        start_date=None,
        end_date=None,
        limit=1,
        order="desc",
    )

    assert len(results) == 1
    assert results[0].date == date(2025, 11, 2)


def test_stock_price_repo_latest_and_by_date(price_repo, sample_stock, sample_prices):
    latest = price_repo.get_latest_price(sample_stock.id)
    by_date = price_repo.get_by_id_and_date(sample_stock.id, date(2025, 11, 1))

    assert latest.date == date(2025, 11, 2)
    assert by_date.close_price == Decimal("3.450000")


def test_stock_price_service_get_prices_validates_stock(price_service):
    with pytest.raises(NotFound):
        price_service.get_prices(9999, None, None, limit=10, order="asc")


def test_stock_price_service_rejects_invalid_date_range(price_service, sample_stock):
    with pytest.raises(BadRequest):
        price_service.get_prices(sample_stock.id, date(2025, 11, 2), date(2025, 11, 1), 10, "asc")


def test_stock_price_service_get_latest_price(price_service, sample_stock, sample_prices):
    latest = price_service.get_latest_price(sample_stock.id)

    assert latest.date == date(2025, 11, 2)


def test_stock_price_service_latest_missing_price_raises(price_service, sample_stock):
    with pytest.raises(NotFound):
        price_service.get_latest_price(sample_stock.id)


def test_stock_price_service_add_price_if_missing(test_db, price_service, sample_stock):
    dto = ExternalStockPriceDTO(
        date=date(2025, 11, 3),
        open_price=Decimal("3.50"),
        high_price=Decimal("3.60"),
        low_price=Decimal("3.45"),
        close_price=Decimal("3.55"),
        volume=130000,
    )

    price_service.add_price_if_missing(sample_stock.id, dto)
    test_db.commit()

    price_service.add_price_if_missing(sample_stock.id, dto)
    test_db.commit()

    prices = test_db.query(StockPrice).filter_by(stock_id=sample_stock.id, date=date(2025, 11, 3)).all()
    assert len(prices) == 1
    assert prices[0].close_price == Decimal("3.550000")


def test_stock_price_api_routes(client, test_db, sample_stock, sample_prices):
    prices = client.get(f"/api/v1/stocks/{sample_stock.id}/prices?limit=10&order=asc")
    latest = client.get(f"/api/v1/stocks/{sample_stock.id}/prices/latest")

    assert prices.status_code == 200
    assert [item["date"] for item in prices.json()] == ["2025-11-01", "2025-11-02"]
    assert latest.status_code == 200
    assert latest.json()["date"] == "2025-11-02"


def test_stock_price_api_missing_stock_returns_404(client):
    assert client.get("/api/v1/stocks/9999/prices").status_code == 404
    assert client.get("/api/v1/stocks/9999/prices/latest").status_code == 404


def test_stock_price_repr_is_readable(sample_prices):
    text = repr(sample_prices[0])

    assert "StockPrice" in text
    assert str(sample_prices[0].stock_id) in text
    assert str(sample_prices[0].date) in text
