from fastapi import APIRouter
from .routers import (
    portfolio,
    positio,
    stocks,
    
    token,
    transactions,
    users,
)

api_router = APIRouter()


api_router.include_router(stocks.router)


api_router.include_router(portfolio.router)
api_router.include_router(positio.router)
api_router.include_router(transactions.router)


api_router.include_router(users.router)
api_router.include_router(token.router)
