from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioRead

def create_portfolio(db: Session, portfolio: PortfolioCreate) -> Portfolio:
    db_portfolio = Portfolio(name=portfolio.name, user_id=portfolio.user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def read_portfolio(db: Session, portfolio_id: int) -> Portfolio | None:
    return db.get(Portfolio, portfolio_id)

def read_positions_from_portfolio(db: Session, portfolio_id: int) -> list:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio:
        return portfolio.positions
    return []

def delete_portfolio(db: Session, portfolio_id: int) -> bool:
    db_portfolio = db.get(Portfolio, portfolio_id)
    if not db_portfolio:
        return False
    db.delete(db_portfolio)
    db.commit()
    return True





