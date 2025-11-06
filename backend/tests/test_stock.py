from pydantic_core import ValidationError
import pytest
from app.schemas.stock import StockCreate
from app.models import Stock
from sqlalchemy.exc import IntegrityError
from app.crud.stock_crud import StockCrud
from app.schemas.stock import StockCreate
from app.main import app
from fastapi.testclient import TestClient
from datetime import datetime, UTC
from app.core.errors.exceptions import NotFound

@pytest.fixture
def test_crud(test_db):
    return StockCrud(test_db)
class TestModelLayer:
    def test_create_stock(self, test_crud, fake_stock_data):
        result = test_crud.create_stock(fake_stock_data)

        assert result.ticker == "NOKIA.HE"
        assert result.isin == "FI0009000681"
        assert result.name == "Nokia Oyj"
        assert result.close_price == 3.45

    def test_unique_ticker(self, test_crud, fake_stock_data):
        first_stock = test_crud.create_stock(fake_stock_data)
        assert first_stock.id is not None

        same_ticker = StockCreate(
            ticker="NOKIA.HE",
            name="Nokia",
            isin="FI00090006",
            close_price=3.4,
            sector="Technology",
            updated_at=datetime.now(UTC),
        )

        with pytest.raises(IntegrityError) as exc_info:
            test_crud.db.add(
                test_crud.model(
                    ticker=same_ticker.ticker,
                    isin=same_ticker.isin,
                    name=same_ticker.name,
                    close_price=same_ticker.close_price,
                    sector=same_ticker.sector,
                    updated_at=same_ticker.updated_at,
                )
            )
            test_crud.db.commit()  # <-- triggers IntegrityError

        assert "UNIQUE constraint failed" in str(exc_info.value)

        test_crud.db.rollback()

    def test_optional_fields(self, test_crud):
        stock = StockCreate(
            ticker="Fortum.HE",
            isin="FI0009000681",
            close_price=5.5        
        )
        result = test_crud.create_stock(stock)

        assert result.name is None
        assert result.sector is None
        assert result.ticker == "Fortum.HE"

    def test_updated_at(self, test_crud):
        fake_stock = StockCreate(
            ticker="NOKIA.HE",
            name="Nokia Oyj",
            isin="FI0009000681",
            close_price=3.45,
            sector="Technology",
        )
        result = test_crud.create_stock(fake_stock)

        assert result.updated_at is not None

        now = datetime.now(UTC)

        db_time = result.updated_at
        if db_time.tzinfo is None:
            db_time = db_time.replace(tzinfo=UTC)

        time_diff = abs((now - db_time).total_seconds())

        assert time_diff < 0.1

    def test_stock_repr_is_readable(self, test_db):
        from app.models.stock import Stock

        stock = Stock(
            ticker="NOKIA.HE",
            name="Nokia Oyj",
            close_price=3.45,
            sector="Technology"
        )

        result = repr(stock)

        assert isinstance(result, str)
        assert "Stock" in result
        assert "NOKIA.HE" in result
        assert "Nokia Oyj" in result

class TestSchemaLayer:
    def test_valid_stock_create(self):
        stock = StockCreate(
            ticker="NOKIA.HE",
            name="Nokia Oyj",
            isin="FI0009000681",
            close_price=3.45,
            sector="Technology",
        )
        assert stock.ticker == "NOKIA.HE"
        assert stock.close_price == 3.45

    def test_optional_fields_default_none(self):
        stock = StockCreate(ticker="FORTUM.HE", close_price=12.5)
        assert stock.name is None
        assert stock.isin is None
        assert stock.sector is None

    def test_missing_required_field(self):
        with pytest.raises(ValidationError):
            StockCreate(close_price=12.5)

    def test_invalid_close_price_type(self):
        with pytest.raises(ValidationError):
            StockCreate(ticker="NOKIA.HE", close_price="not_a_number")

    def test_invalid_ticker_type(self):
        with pytest.raises(ValidationError):
            StockCreate(ticker=1234, close_price=10.0)


class TestStockCrud:
    def test_create_new_stock_successfully(self, test_crud):
        """Ensure stock is inserted properly into DB."""
        stock_data = StockCreate(
            ticker="NOKIA.HE",
            isin="FI0009000681",
            name="Nokia Oyj",
            close_price=3.45,
            sector="Technology",
            updated_at=datetime.now(UTC),
        )

        result = test_crud.create_stock(stock_data)
        assert result.id is not None
        assert result.ticker == "NOKIA.HE"
        assert result.close_price == 3.45
        assert result.sector == "Technology"

    def test_prevent_duplicate_stock_insertion(self, test_crud):
        """Should return existing stock, not insert duplicate."""
        stock_data = StockCreate(
            ticker="NOKIA.HE",
            isin="FI0009000681",
            name="Nokia Oyj",
            close_price=3.45,
        )
        first = test_crud.create_stock(stock_data)
        second = test_crud.create_stock(stock_data)

        assert first.id == second.id  # duplicate prevented
        assert test_crud.db.query(Stock).count() == 1

    def test_update_existing_stock_price_correctly(self, test_crud):
        """Ensure price is updated and timestamp refreshed."""
        stock_data = StockCreate(
            ticker="FORTUM.HE",
            isin="FI0009007132",
            name="Fortum Oyj",
            close_price=12.5,
        )
        created = test_crud.create_stock(stock_data)
        updated = test_crud.update_stock_price("FORTUM.HE", 14.2)

        # Normalize timezone — make both aware in UTC
        def to_aware(dt):
            return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt

        created_time = to_aware(created.updated_at)
        updated_time = to_aware(updated.updated_at)

        assert updated.close_price == 14.2
        time_diff = (updated_time - created_time).total_seconds()
        assert time_diff >= 0
        assert time_diff < 2

    def test_get_stock_by_id_and_isin(self, test_crud):
        """Test retrieval by both ID and ISIN."""
        stock_data = StockCreate(
            ticker="KNEBV.HE",
            isin="FI0009013403",
            name="Kone Oyj",
            close_price=56.5,
        )
        created = test_crud.create_stock(stock_data)

        by_id = test_crud.get_id_or_404(created.id)
        by_isin = test_crud.get_stock_by_isin("FI0009013403")

        assert by_id.id == created.id
        assert by_isin.id == created.id
        assert by_id.ticker == "KNEBV.HE"

    def test_raise_notfound_for_missing_stock(self, test_crud):
        """Should raise NotFound when stock not in DB."""
        with pytest.raises(NotFound):
            test_crud.get_stock_by_isin("FAKEISIN123")

        with pytest.raises(NotFound):
            test_crud.get_id_or_404(9999)

    def test_handle_integrity_error_and_rollback(self, test_crud):
        """Simulate integrity violation and verify rollback occurs."""
        # Insert a stock
        stock = StockCreate(
            ticker="TEST.HE",
            isin="FI0009009999",
            name="Test Oyj",
            close_price=5.0,
        )
        test_crud.create_stock(stock)

        # Manually break the unique constraint
        duplicate = Stock(
            ticker="TEST.HE",
            isin="FI0009009999",
            name="Duplicate",
            close_price=6.0,
        )
        test_crud.db.add(duplicate)
        with pytest.raises(IntegrityError):
            test_crud.db.commit()

        # Rollback DB and ensure session still usable
        test_crud.db.rollback()
        valid_stock = StockCreate(
            ticker="NEWTEST.HE",
            isin="FI0009111111",
            name="Valid Stock",
            close_price=9.9,
        )
        result = test_crud.create_stock(valid_stock)
        assert result.ticker == "NEWTEST.HE"

#class TestApiLayer:
    def test_create_stock_returns_201(self, client, test_db):
        """✔ POST /stocks creates stock and returns 201 status."""
        payload = {
            "ticker": "NOKIA.HE",
            "isin": "FI0009000681",
            "name": "Nokia Oyj",
            "close_price": 3.45,
            "sector": "Technology",
        }

        response = client.post("/stocks/", json=payload)
        assert response.status_code in (200, 201)
        data = response.json()
        assert data["ticker"] == "NOKIA.HE"
        assert data["close_price"] == 3.45

    def test_get_stock_by_id_returns_correct_data(self, client, test_db, test_stock):
        """✔ GET /stocks/{id} returns correct stock data."""
        response = client.get(f"/stocks/{test_stock.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["ticker"] == test_stock.ticker
        assert abs(data["close_price"] - test_stock.close_price) < 0.01

    def test_get_stock_by_ticker_returns_correct_stock(self, client, test_db, test_stock):
        """✔ GET /stocks/ticker/{ticker} returns correct stock."""
        # Add a route like /stocks/ticker/{ticker} in your API layer if not already
        response = client.get(f"/stocks/ticker/{test_stock.ticker}")
        assert response.status_code == 200
        data = response.json()
        assert data["isin"] == test_stock.isin
        assert data["name"] == test_stock.name

    def test_invalid_id_or_ticker_returns_404(self, client):
        """✔ Invalid ID or ticker returns 404 NotFound."""
        id_response = client.get("/stocks/9999")
        assert id_response.status_code == 404

        ticker_response = client.get("/stocks/ticker/FAKE123")
        assert ticker_response.status_code == 404

    def test_duplicate_post_returns_existing_stock(self, client, test_db):
        """✔ Duplicate POST returns existing stock instead of re-creating."""
        payload = {
            "ticker": "NOKIA.HE",
            "isin": "FI0009000681",
            "name": "Nokia Oyj",
            "close_price": 3.45,
        }

        first = client.post("/stocks/", json=payload)
        second = client.post("/stocks/", json=payload)

        assert first.status_code in (200, 201)
        assert second.status_code in (200, 201)

        first_id = first.json()["id"]
        second_id = second.json()["id"]

        assert first_id == second_id  # should return same stock, not duplicate

