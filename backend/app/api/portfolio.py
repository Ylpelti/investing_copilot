from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.db.session import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioRead
from app.models.user import User
from app.crud import portfolio_crud
from fastapi import UploadFile
from app.security.dependencies import get_current_user

router = APIRouter(
        prefix="/portfolios",
        tags=["portfolios"],
    )

@router.post("/", response_model=PortfolioRead)
def create_portfolio(portfolio: PortfolioCreate, session: Session = Depends(get_db)):
    return portfolio_crud.create_portfolio(session, portfolio)

@router.post("/{portfolio.id}/import")
def import_portfolio(portfolio_id: int, file: UploadFile, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    portfolio = portfolio_crud.read_portfolio(db, portfolio_id, current_user)
    
    
    from app.services.portfolio_import_service import parse_csv
    parse_csv(file, portfolio_id, db) # type: ignore
    
    return {"detail": "Import functionality not yet implemented"}

@router.get("/{portfolio_id}", response_model=PortfolioRead)
def read_portfolio(portfolio_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    portfolio = portfolio_crud.read_portfolio(session, portfolio_id, current_user)
    
    return portfolio

@router.get("/user/{user_id}", response_model=list[PortfolioRead])
def read_user_portfolios(user_id: int, session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.portfolios
