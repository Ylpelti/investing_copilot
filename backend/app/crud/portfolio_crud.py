from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioRead
from fastapi import HTTPException


def create_portfolio(db: Session, portfolio: PortfolioCreate) -> PortfolioRead:
    db_portfolio = Portfolio(name=portfolio.name, user_id=portfolio.user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def read_portfolio(db: Session, portfolio_id: int, current_user) -> PortfolioRead | None:
    portfolio = db.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if portfolio.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to import into this portfolio")

def read_positions_from_portfolio(db: Session, portfolio_id: int) -> list:
    portfolio = db.get(Portfolio, portfolio_id)
    if portfolio and portfolio.positions:
        return portfolio.positions
    return []

def delete_portfolio(db: Session, portfolio_id: int) -> bool:
    db_portfolio = db.get(Portfolio, portfolio_id)
    if not db_portfolio:
        return False
    db.delete(db_portfolio)
    db.commit()
    return True


