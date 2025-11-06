import pytest
from datetime import date, datetime, timedelta
from app.models import Stock, StockPrice
from app.crud.stock_prices_crud import StockPriceCrud
from app.core.errors.exceptions import NotFound, BadRequest


@pytest.fixture
def test_crud(test_db):
    return StockPriceCrud(test_db)


@pytest.fixture
def sample_stock(test_db):
    """Create a stock to attach prices to."""
    stock = Stock(
        ticker="NOKIA.HE",
        isin="FI0009000681",
        name="Nokia Oyj",
        close_price=3.45,
        sector="Technology",
    )
    test_db.add(stock)
    test_db.commit()
    test_db.refresh(stock)
    return stock


@pytest.fixture
def sample_prices(test_db, sample_stock):
    """Insert a few prices for the sample stock."""
    prices = [
        StockPrice(
            stock_id=sample_stock.id,
            date=date(2025, 11, 1),
            open_price=3.40,
            high_price=3.50,
            low_price=3.35,
            close_price=3.45,
            volume=100000,
        ),
        StockPrice(
            stock_id=sample_stock.id,
            date=date(2025, 11, 2),
            open_price=3.45,
            high_price=3.55,
            low_price=3.40,
            close_price=3.50,
            volume=120000,
        ),
    ]
    test_db.add_all(prices)
    test_db.commit()
    return prices


class TestStockPriceCrud:
    def test_read_stock_price_success(self, test_crud, sample_prices):
        """Ensure we can read an existing stock price."""
        first_price = sample_prices[0]
        result = test_crud.read_stock_price(first_price.id)
        assert result.id == first_price.id
        assert result.close_price == pytest.approx(3.45, rel=1e-6)

    def test_read_stock_price_not_found(self, test_crud):
        """Ensure NotFound is raised for invalid ID."""
        with pytest.raises(NotFound) as exc_info:
            test_crud.read_stock_price(9999)
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.message.lower()

    def test_read_stock_prices_by_stock_id(self, test_crud, sample_stock, sample_prices):
        """Retrieve all prices for a stock and confirm order by date."""
        results = test_crud.read_stock_prices_by_stock_id(sample_stock.id)
        assert len(results) == len(sample_prices)
        assert results[0].date < results[1].date

    def test_read_stock_prices_by_ticker(self, test_crud, sample_prices):
        """Retrieve prices via ticker join."""
        results = test_crud.read_stock_prices_by_ticker("NOKIA.HE")
        assert len(results) == 2
        assert all(p.stock.ticker == "NOKIA.HE" for p in results)

    def test_read_stock_prices_by_ticker_not_found(self, test_crud):
        """Empty list for non-existent ticker should raise NotFound."""
        with pytest.raises(NotFound):
            test_crud.read_stock_prices_by_ticker("INVALID")

    def test_read_stock_prices_by_date_range_valid(self, test_crud, sample_stock, sample_prices):
        """Ensure date filtering returns correct subset."""
        start = "2025-11-01"
        end = "2025-11-02"
        results = test_crud.read_stock_prices_by_date_range(sample_stock.id, start, end)
        assert len(results) == 2
        assert all(isinstance(p.date, date) for p in results)

    def test_read_stock_prices_by_date_range_invalid_format(self, test_crud, sample_stock):
        """Invalid date strings raise BadRequest."""
        with pytest.raises(BadRequest) as exc_info:
            test_crud.read_stock_prices_by_date_range(sample_stock.id, "invalid-date", "2025-11-01")
        assert exc_info.value.status_code == 400
        assert "invalid date format" in exc_info.value.message.lower()

    def test_read_stock_prices_by_date_range_start_after_end(self, test_crud, sample_stock):
        """Start date after end date should raise BadRequest."""
        with pytest.raises(BadRequest) as exc_info:
            test_crud.read_stock_prices_by_date_range(
                sample_stock.id, "2025-11-10", "2025-11-01"
            )
        assert exc_info.value.status_code == 400
        assert "before end_date" in exc_info.value.message.lower()

    def test_read_stock_prices_by_date_range_no_data(self, test_crud, sample_stock):
        """Empty range with no matching data should raise NotFound."""
        with pytest.raises(NotFound) as exc_info:
            test_crud.read_stock_prices_by_date_range(
                sample_stock.id, "2024-01-01", "2024-01-05"
            )
        assert exc_info.value.status_code == 404
        assert "no prices found" in exc_info.value.message.lower()

    def test_repr_is_readable(self, sample_prices):
        """Confirm __repr__ returns a readable summary."""
        text = repr(sample_prices[0])
        assert isinstance(text, str)
        assert "Stock" in text
        assert str(sample_prices[0].stock_id) in text
        assert str(sample_prices[0].date) in text
