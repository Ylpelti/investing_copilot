from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.db.session import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioUpdate
from app.models.user import User
from app.crud.portfolio_crud import PortfolioCrud
from fastapi import UploadFile
from app.security.dependencies import get_current_user
from app.services.portfolio_import_service import parse_csv

router = APIRouter(
        prefix="/portfolios",
        tags=["portfolios"],
    )


@router.post("/", response_model=PortfolioRead)
def create_portfoio(
    portfolio_in: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud = PortfolioCrud(db)
    portfolio_in.user_id = current_user.id
    return crud.create_portfolio(portfolio_in)

@router.get("/{portfolio.id}", response_model=PortfolioRead)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PortfolioCrud(db)
    return crud.get_owned_portfolio(portfolio_id=portfolio_id, user_id=current_user.id)

@router.put("/{portfolio.id}", response_model=PortfolioRead)
def update_portfolio(portfolio_id: int, portfolio_in: PortfolioUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PortfolioCrud(db)
    return crud.update_portfolio(portfolio_id=portfolio_id, portfolio_in=portfolio_in, current_user_id=current_user.id)

@router.delete("/{portfolio.id}", status_code=204)
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PortfolioCrud(db)
    return crud.delete_portfolio(portfolio_id=portfolio_id, current_user_id=current_user.id)

@router.post("/{portfolio.id}/import", response_model=PortfolioRead)
def import_portfolio(
    portfolio_id:int,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud = PortfolioCrud(db)
    portfolio = crud.get_owned_portfolio(portfolio_id=portfolio_id, user_id=current_user.id)

    parse_csv(file, portfolio.id, db, current_user.id) #type: ignore

    return {"detail": "Import completed successfully."}

@router.post("/{portfolio.id}/explain")
def explain_portfolio(portfolio_id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    







