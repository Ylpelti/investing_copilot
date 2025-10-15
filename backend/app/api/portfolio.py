from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.db.session import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioRead
from app.models.user import User
from app.crud import portfolio_crud

router = APIRouter(
        prefix="/portfolios",
        tags=["portfolios"],
    )

@router.post("/", response_model=PortfolioRead)
def create_portfolio(portfolio: PortfolioCreate, session: Session = Depends(get_db)):
    return portfolio_crud.create_portfolio(session, portfolio)

@router.get("/{portfolio_id}", response_model=PortfolioRead)
def read_portfolio(portfolio_id: int, session: Session = Depends(get_db)):
    portfolio = portfolio_crud.read_portfolio(session, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.get("/user/{user_id}", response_model=list[PortfolioRead])
def read_user_portfolios(user_id: int, session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.portfolios

