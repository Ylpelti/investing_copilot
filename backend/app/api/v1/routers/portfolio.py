from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.portfolio.portfolio_service import PortfolioService
from app.db.session import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioUpdate
from app.models.user import User
from app.crud.transaction_crud import TransactionCrud
from fastapi import UploadFile
from app.security.dependencies import get_current_user
from app.services.portfolio.dependencies import get_portfolio_import_service 
from app.services.portfolio.portfolio_explanation_service import PortfolioExplanationService
from app.services.portfolio.dependencies import get_portfolio_explanation_service, get_portfolio_analytics_service, get_portfolio_services
from typing import List
from app.schemas.positio import PositionRead
from typing import TextIO

from app.services.portfolio.portfolio_analytics_service import PortfolioAnalyticsService
from app.services.portfolio.portfolio_import_service import PortfolioImportService

router = APIRouter(
        prefix="/portfolios",
        tags=["portfolios"],
    )

@router.post("/", response_model=PortfolioRead)
def create_portfolio(
    portfolio_in: PortfolioCreate,
    portfolio_services: PortfolioService = Depends(get_portfolio_services)
):
    return portfolio_services.create_portfolio(portfolio_in)

@router.get("/me", response_model=List[PortfolioRead])
def get_portfolio_list(
    portfolio_services: PortfolioService = Depends(get_portfolio_services)):
    return portfolio_services.get_user_owned_portfolios()

@router.get("/{portfolio_id}", response_model=PortfolioRead)
def get_portfolio(
    portfolio_id: int,
    portfolio_services: PortfolioService = Depends(get_portfolio_services)
  ):
    return portfolio_services.get_owned_portfolio_or_404(portfolio_id)

@router.put("/{portfolio_id}", response_model=PortfolioRead)
def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    portfolio_service: PortfolioService = Depends(get_portfolio_services)):
    return portfolio_service.update_portfolio(portfolio_data, portfolio_id)

@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(
    portfolio_id: int,
    portfolio_service: PortfolioService = Depends(get_portfolio_services)
):
    return portfolio_service.delete_portfolio(portfolio_id)

@router.post("/{portfolio_id}/import", response_model=PortfolioRead)
def import_portfolio(
    portfolio_id: int,
    file: UploadFile,
    portfolio_import_service: PortfolioImportService = Depends(get_portfolio_import_service)
):
    return portfolio_import_service.import_csv(file.file, portfolio_id)

@router.post("/{portfolio_id}/explain")
def explain_portfolio(
    portfolio_id:int,
    portfolio_explain_service: PortfolioExplanationService = Depends(get_portfolio_explanation_service)
):
    explanation =  portfolio_explain_service.explain_portfolio(portfolio_id)
    return {
        "portfolio_id": portfolio_id,
        "explanation": explanation
    }

@router.get("/{portfolio_id}/positions", response_model=List[PositionRead])
def get_portfolio_positions(
    portfolio_id:int,
    portfolio_services: PortfolioService = Depends(get_portfolio_services)
):
    return portfolio_services.get_portfolio_positions(portfolio_id)

@router.get("/{portfolio_id}/charts")
def get_portfolio_nav(
    portfolio_id:int,
    analytics_service: PortfolioAnalyticsService = Depends(get_portfolio_analytics_service)
):
    return analytics_service.calculate_nav(portfolio_id)