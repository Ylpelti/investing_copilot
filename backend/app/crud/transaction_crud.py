from app.crud.base_crud import BaseCrud
from app.models.transaction import PortfolioTransaction
from app.models.transaction import PortfolioTransaction



class TransactionCrud(BaseCrud):
    model = PortfolioTransaction

    def add(self, tx: PortfolioTransaction):
        return self.db.add(tx)

    def get_by_portfolio(self, portfolio_id: int) -> list[PortfolioTransaction]:
        return (
            self.db.query(PortfolioTransaction)
            .filter(
                PortfolioTransaction.portfolio_id == portfolio_id)
                .order_by(PortfolioTransaction.timestamp.desc())
                .all()
        )

    