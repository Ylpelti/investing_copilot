import pytest
from datetime import datetime
from app.crud.transaction_crud import TransactionCrud
from app.models.transaction import TransactionType, PortfolioTransaction
from app.core.errors.exceptions import BadRequest, NotFound, Forbidden
from app.schemas.transactions import TransactionCreate
from app.models import Position


@pytest.fixture
def test_crud(test_db):
    """Provide a TransactionCrud instance bound to the test database."""
    return TransactionCrud(test_db)


@pytest.fixture
def test_position(test_db, test_portfolio, test_stock):
    """Existing position used to test sell logic."""
    pos = Position(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        symbol=test_stock.ticker,
        quantity=10,
        buy_price=100.0,
    )
    test_db.add(pos)
    test_db.commit()
    test_db.refresh(pos)
    return pos


class TestTransactionCrud:
    def test_create_buy_transaction_creates_position(
        self, test_crud, test_portfolio, test_stock, test_user
    ):
        """Buying new stock should create a new position and transaction record."""
        tx = TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            symbol=test_stock.ticker,
            type=TransactionType.BUY,
            quantity=5,
            price=100.0,
            timestamp=datetime(2025, 1, 1),
        )

        created_tx = test_crud.ceate_transaction(tx, test_user.id)
        assert created_tx.id is not None
        assert created_tx.type == TransactionType.BUY
        assert created_tx.total_value == pytest.approx(500.0, rel=1e-6)

        # Verify position updated
        pos = (
            test_crud.db.query(Position)
            .filter_by(portfolio_id=test_portfolio.id, stock_id=test_stock.id)
            .first()
        )
        assert pos is not None
        assert pos.quantity == 5
        assert pos.buy_price == 100.0

    def test_create_buy_transaction_updates_existing_position(
        self, test_crud, test_position, test_user
    ):
        """Buying more of same stock should update average buy price."""
        tx = TransactionCreate(
            portfolio_id=test_position.portfolio_id,
            stock_id=test_position.stock_id,
            symbol=test_position.symbol,
            type=TransactionType.BUY,
            quantity=10,
            price=200.0,
            timestamp=datetime(2025, 2, 1),
        )

        created_tx = test_crud.ceate_transaction(tx, test_user.id)
        assert created_tx.id is not None
        assert created_tx.total_value == pytest.approx(2000.0, rel=1e-6)

        updated = (
            test_crud.db.query(Position)
            .filter_by(portfolio_id=test_position.portfolio_id, stock_id=test_position.stock_id)
            .first()
        )
        assert updated.quantity == 20
        assert updated.buy_price == pytest.approx(150.0, rel=1e-6)  # weighted average

    def test_create_sell_transaction_reduces_position(
        self, test_crud, test_position, test_user
    ):
        """Selling shares should reduce quantity."""
        tx = TransactionCreate(
            portfolio_id=test_position.portfolio_id,
            stock_id=test_position.stock_id,
            symbol=test_position.symbol,
            type=TransactionType.SELL,
            quantity=5,
            price=150.0,
            timestamp=datetime(2025, 3, 1),
        )

        tx_result = test_crud.ceate_transaction(tx, test_user.id)
        assert tx_result.type == TransactionType.SELL

        updated = (
            test_crud.db.query(Position)
            .filter_by(portfolio_id=test_position.portfolio_id, stock_id=test_position.stock_id)
            .first()
        )
        assert updated.quantity == 5

    def test_sell_too_many_raises(self, test_crud, test_position, test_user):
        """Selling more than owned should raise BadRequest."""
        tx = TransactionCreate(
            portfolio_id=test_position.portfolio_id,
            stock_id=test_position.stock_id,
            symbol=test_position.symbol,
            type=TransactionType.SELL,
            quantity=50,
            price=150.0,
            timestamp=datetime(2025, 3, 1),
        )
        with pytest.raises(BadRequest):
            test_crud.ceate_transaction(tx, test_user.id)

    def test_sell_nonexistent_position_raises(self, test_crud, test_portfolio, test_stock, test_user):
        """Selling a stock not owned should raise NotFound."""
        tx = TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            symbol=test_stock.ticker,
            type=TransactionType.SELL,
            quantity=5,
            price=100.0,
            timestamp=datetime(2025, 4, 1),
        )
        with pytest.raises(NotFound):
            test_crud.ceate_transaction(tx, test_user.id)

    def test_get_portfolio_transactions(self, test_crud, test_portfolio, test_stock, test_user):
        """Should list all transactions for a portfolio."""
        # Add a few transactions
        for i in range(3):
            tx = TransactionCreate(
                portfolio_id=test_portfolio.id,
                stock_id=test_stock.id,
                symbol=test_stock.ticker,
                type=TransactionType.BUY,
                quantity=1,
                price=100 + i,
                timestamp=datetime(2025, 1, i + 1),
            )
            test_crud.ceate_transaction(tx, test_user.id)

        results = test_crud.get_portfolio_transactions(test_portfolio.id, test_user.id)
        assert len(results) == 3
        assert all(isinstance(t, PortfolioTransaction) for t in results)
        assert results[0].timestamp >= results[1].timestamp  # Sorted desc

def test_buy_transaction_creates_transaction_and_updates_position(test_crud, test_portfolio, test_stock, test_user):
    tx = TransactionCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        symbol=test_stock.ticker,
        type=TransactionType.BUY,
        quantity=10,
        price=50.0,
        timestamp=datetime(2025, 5, 1),
    )
    created = test_crud.ceate_transaction(tx, test_user.id)

    # Transaction stored
    db_tx = test_crud.db.get(PortfolioTransaction, created.id)
    assert db_tx is not None
    assert db_tx.total_value == pytest.approx(500.0, rel=1e-6)

    # Position updated
    pos = test_crud.db.query(Position).filter_by(stock_id=test_stock.id).first()
    assert pos.quantity == 10

def test_transaction_rolls_back_on_integrity_error(monkeypatch, test_crud, test_portfolio, test_stock, test_user):
    def broken_flush(): raise Exception("DB flush failed")
    monkeypatch.setattr(test_crud.db, "flush", broken_flush)

    tx = TransactionCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        symbol=test_stock.ticker,
        type=TransactionType.BUY,
        quantity=10,
        price=50.0,
        timestamp=datetime(2025, 5, 1),
    )

    with pytest.raises(BadRequest):
        test_crud.ceate_transaction(tx, test_user.id)

    # Nothing committed
    txs = test_crud.db.query(PortfolioTransaction).all()
    assert txs == []

def test_transaction_on_non_owned_portfolio_raises_forbidden(test_crud, test_db, test_stock, test_user):
    from app.models import Portfolio, User

    other_user = User(username="evil", email="evil@example.com", pw_hash="123")
    test_db.add(other_user)
    test_db.commit()

    foreign_portfolio = Portfolio(name="Not yours", user_id=other_user.id)
    test_db.add(foreign_portfolio)
    test_db.commit()

    tx = TransactionCreate(
        portfolio_id=foreign_portfolio.id,
        stock_id=test_stock.id,
        symbol=test_stock.ticker,
        type=TransactionType.BUY,
        quantity=5,
        price=120.0,
        timestamp=datetime(2025, 5, 1),
    )

    with pytest.raises(Forbidden):
        test_crud.ceate_transaction(tx, test_user.id)

@pytest.mark.parametrize("quantity,price", [(0, 10), (-5, 10), (5, -1)])
def test_invalid_transaction_values_raise(test_crud, test_portfolio, test_stock, test_user, quantity, price):
    tx = TransactionCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        symbol=test_stock.ticker,
        type=TransactionType.BUY,
        quantity=quantity,
        price=price,
        timestamp=datetime(2025, 5, 1),
    )
    with pytest.raises(BadRequest):
        test_crud.ceate_transaction(tx, test_user.id)


def test_full_liquidation_removes_position(test_crud, test_position, test_user):
    tx = TransactionCreate(
        portfolio_id=test_position.portfolio_id,
        stock_id=test_position.stock_id,
        symbol=test_position.symbol,
        type=TransactionType.SELL,
        quantity=test_position.quantity,
        price=200.0,
        timestamp=datetime(2025, 5, 1),
    )
    created_tx = test_crud.ceate_transaction(tx, test_user.id)

    assert created_tx.type == TransactionType.SELL
    deleted = test_crud.db.query(Position).filter_by(id=test_position.id).first()
    assert deleted is None


def test_transactions_return_sorted_desc(test_crud, test_portfolio, test_stock, test_user):
    for i in range(3):
        tx = TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            symbol=test_stock.ticker,
            type=TransactionType.BUY,
            quantity=1,
            price=100 + i,
            timestamp=datetime(2025, 5, 1 + i),
        )
        test_crud.ceate_transaction(tx, test_user.id)

    txs = test_crud.get_portfolio_transactions(test_portfolio.id, test_user.id)
    timestamps = [t.timestamp for t in txs]
    assert timestamps == sorted(timestamps, reverse=True)


def test_position_matches_sum_of_transactions(test_crud, test_portfolio, test_stock, test_user):
    # Buy twice
    for q, p in [(5, 100), (5, 200)]:
        tx = TransactionCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            symbol=test_stock.ticker,
            type=TransactionType.BUY,
            quantity=q,
            price=p,
            timestamp=datetime(2025, 5, 1),
        )
        test_crud.ceate_transaction(tx, test_user.id)

    pos = test_crud.db.query(Position).filter_by(portfolio_id=test_portfolio.id).first()
    txs = test_crud.db.query(PortfolioTransaction).filter_by(portfolio_id=test_portfolio.id).all()
    total_bought = sum(t.quantity for t in txs if t.type == TransactionType.BUY)
    total_sold = sum(t.quantity for t in txs if t.type == TransactionType.SELL)
    assert pos.quantity == total_bought - total_sold

