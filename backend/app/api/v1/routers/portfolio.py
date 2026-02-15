from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.db.session import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioUpdate
from app.models.user import User
from app.crud.portfolio_crud import PortfolioCrud
from app.crud.transaction_crud import TransactionCrud
from fastapi import UploadFile
from app.security.dependencies import get_current_user
from app.services.portfolio_import_service import parse_csv
from app.services.portfolio_explanation_service import PortfolioExplanationService
from app.services.dependencies import get_portfolio_explanation_service
from typing import List
from app.crud.position_crud import PositionCrud
from app.schemas.positio import PositionRead
from app.services.dependencies import get_portfolio_analytics_service
from app.services.portfolio_analytics_service import PortfolioAnalyticsService
from app.core.utils.series_to_records import series_to_record


router = APIRouter(
        prefix="/portfolios",
        tags=["portfolios"],
    )


@router.post("/", response_model=PortfolioRead)
def create_portfolio(
    portfolio_in: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud = PortfolioCrud(db)
    portfolio_in.user_id = current_user.id
    return crud.create_portfolio(portfolio_in)

@router.get("/me", response_model=List[PortfolioRead])
def get_portfolio_list(db: Session = Depends(get_db), currrent_user: User = Depends(get_current_user)):
    crud = PortfolioCrud(db)
    return crud.get_user_owned_portfolios(currrent_user.id)

@router.get("/{portfolio_id}", response_model=PortfolioRead)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PortfolioCrud(db)
    return crud.get_owned_portfolio(portfolio_id=portfolio_id, user_id=current_user.id)

@router.put("/{portfolio_id}", response_model=PortfolioRead)
def update_portfolio(portfolio_id: int, portfolio_in: PortfolioUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PortfolioCrud(db)
    return crud.update_portfolio(portfolio_id=portfolio_id, portfolio_in=portfolio_in, current_user_id=current_user.id)

@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    crud = PortfolioCrud(db)
    return crud.delete_portfolio(portfolio_id=portfolio_id, current_user_id=current_user.id)

@router.post("/{portfolio_id}/import", response_model=PortfolioRead)
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

@router.post("/{portfolio_id}/explain")
def explain_portfolio(
    portfolio_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: PortfolioExplanationService = Depends(get_portfolio_explanation_service)):
    transaction_crud = TransactionCrud(db)
    txs = transaction_crud.get_portfolio_transactions(portfolio_id=portfolio_id, current_user_id=current_user.id)

    explanation = service.explain_portfolio(txs, db)

    return {
        "portfolio_id": portfolio_id,
        "explanation": explanation
    }

@router.get("/{portfolio_id}/positions", response_model=List[PositionRead])
def get_portfolio_positions(
    portfolio_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    position_crud = PositionCrud(db)
    return position_crud.get_portfolio_positions(portfolio_id, current_user.id)

@router.get("/{portfolio_id}/charts")
def get_portfolio_timeseries(portfolio_id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), analytics_service:PortfolioAnalyticsService = Depends(get_portfolio_analytics_service)):
    transaction_crud = TransactionCrud(db)
    txs = transaction_crud.get_portfolio_transactions(portfolio_id, current_user)
    nav = PortfolioAnalyticsService.calculate_nav(analytics_service, txs, db)
    return series_to_record(nav)






