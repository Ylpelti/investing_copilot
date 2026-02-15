from fastapi import APIRouter
from .routers import (
    portfolio,
    positio,
    stocks,
    stocks_price,
    token,
    transactions,
    users,
)

api_router = APIRouter()

# Core domain
api_router.include_router(stocks.router)
api_router.include_router(stocks_price.router)

# Portfolio domain
api_router.include_router(portfolio.router)
api_router.include_router(positio.router)
api_router.include_router(transactions.router)

# Auth & users
api_router.include_router(users.router)
api_router.include_router(token.router)
