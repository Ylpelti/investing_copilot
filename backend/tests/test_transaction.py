from datetime import datetime
from decimal import Decimal

import pytest

from app.core.errors.exceptions import BadRequest, Forbidden
from app.crud.portfolio_crud import PortfolioCrud
from app.crud.position_crud import PositionCrud
from app.crud.stock_crud import StockCrud
from app.crud.transaction_crud import TransactionCrud
from app.models import Portfolio, Position, User
from app.models.transaction import TransactionType
from app.schemas.transactions import TransactionCreate
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.position.position_service import PositionService
from app.services.stocks.stock_service import StockService
from app.services.transaction.transaction_service import TransactionService


@pytest.fixture
def transaction_service(test_db, test_user):
    tx_repo = TransactionCrud(test_db)
    position_service = PositionService(PositionCrud(test_db))
    portfolio_service = PortfolioService(
        db=test_db,
        current_user_id=test_user.id,
        portfolio_repo=PortfolioCrud(test_db),
        position_repo=PositionCrud(test_db),
    )
    stock_service = StockService(stock_repo=StockCrud(test_db), db=test_db)
    return TransactionService(
        db=test_db,
        tx_repo=tx_repo,
        position_service=position_service,
        portfolio_service=portfolio_service,
        stock_service=stock_service,
    )


def test_create_buy_transaction_creates_position(transaction_service, test_portfolio, test_stock, test_db):
    tx = TransactionCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        type=TransactionType.BUY,
        quantity=Decimal("5"),
        price=Decimal("100"),
        timestamp=datetime(2025, 1, 1),
    )
    created = transaction_service.create_transaction(tx)
    assert created.id is not None
    assert created.total_value == Decimal("500")

    pos = (
        test_db.query(Position)
        .filter_by(portfolio_id=test_portfolio.id, stock_id=test_stock.id)
        .first()
    )
    assert pos is not None
    assert pos.quantity == Decimal("5")
    assert pos.buy_price == Decimal("100")


def test_buy_updates_existing_position_weighted_avg(transaction_service, test_portfolio, test_stock, test_db):
    first = TransactionCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        type=TransactionType.BUY,
        quantity=Decimal("10"),
        price=Decimal("100"),
        timestamp=datetime(2025, 1, 1),
    )
    second = TransactionCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        type=TransactionType.BUY,
        quantity=Decimal("10"),
        price=Decimal("200"),
        timestamp=datetime(2025, 1, 2),
    )
    transaction_service.create_transaction(first)
    transaction_service.create_transaction(second)

    pos = (
        test_db.query(Position)
        .filter_by(portfolio_id=test_portfolio.id, stock_id=test_stock.id)
        .first()
    )
    assert pos.quantity == Decimal("20")
    assert pos.buy_price == Decimal("150")


def test_sell_reduces_and_full_liquidation_removes_position(
    transaction_service, test_portfolio, test_stock, test_db
):
    transaction_service.create_transaction(
        TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            type=TransactionType.BUY,
            quantity=Decimal("10"),
            price=Decimal("100"),
            timestamp=datetime(2025, 1, 1),
        )
    )
    transaction_service.create_transaction(
        TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            type=TransactionType.SELL,
            quantity=Decimal("4"),
            price=Decimal("120"),
            timestamp=datetime(2025, 1, 2),
        )
    )
    pos = (
        test_db.query(Position)
        .filter_by(portfolio_id=test_portfolio.id, stock_id=test_stock.id)
        .first()
    )
    assert pos is not None
    assert pos.quantity == Decimal("6")

    transaction_service.create_transaction(
        TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            type=TransactionType.SELL,
            quantity=Decimal("6"),
            price=Decimal("120"),
            timestamp=datetime(2025, 1, 3),
        )
    )
    removed = (
        test_db.query(Position)
        .filter_by(portfolio_id=test_portfolio.id, stock_id=test_stock.id)
        .first()
    )
    assert removed is None


def test_invalid_values_raise_bad_request(transaction_service, test_portfolio, test_stock):
    with pytest.raises(BadRequest):
        transaction_service.create_transaction(
            TransactionCreate(
                portfolio_id=test_portfolio.id,
                stock_id=test_stock.id,
                type=TransactionType.BUY,
                quantity=Decimal("0"),
                price=Decimal("10"),
                timestamp=datetime(2025, 1, 1),
            )
        )


def test_forbidden_on_foreign_portfolio(transaction_service, test_db, test_stock):
    other_user = User(username="foreign", email="foreign@example.com", pw_hash="hash")
    test_db.add(other_user)
    test_db.commit()
    test_db.refresh(other_user)
    foreign_portfolio = Portfolio(name="foreign", user_id=other_user.id, description=None)
    test_db.add(foreign_portfolio)
    test_db.commit()
    test_db.refresh(foreign_portfolio)

    with pytest.raises(Forbidden):
        transaction_service.create_transaction(
            TransactionCreate(
                portfolio_id=foreign_portfolio.id,
                stock_id=test_stock.id,
                type=TransactionType.BUY,
                quantity=Decimal("1"),
                price=Decimal("10"),
                timestamp=datetime(2025, 1, 1),
            )
        )


def test_get_portfolio_transactions_sorted_desc(transaction_service, test_portfolio, test_stock):
    transaction_service.create_transaction(
        TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            type=TransactionType.BUY,
            quantity=Decimal("1"),
            price=Decimal("10"),
            timestamp=datetime(2025, 1, 1),
        )
    )
    transaction_service.create_transaction(
        TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            type=TransactionType.BUY,
            quantity=Decimal("1"),
            price=Decimal("10"),
            timestamp=datetime(2025, 1, 3),
        )
    )
    txs = transaction_service.get_portfolio_transactions(test_portfolio.id)
    assert len(txs) == 2
    assert txs[0].timestamp >= txs[1].timestamp


def test_create_transaction_api(client, auth_headers, test_portfolio, test_stock):
    response = client.post(
        "/api/v1/transactions/",
        headers=auth_headers,
        json={
            "portfolio_id": test_portfolio.id,
            "stock_id": test_stock.id,
            "type": "BUY",
            "quantity": "2",
            "price": "10",
            "timestamp": "2025-01-01T00:00:00",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == test_portfolio.id
    assert body["stock_id"] == test_stock.id
