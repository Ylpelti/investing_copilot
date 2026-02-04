from fastapi import FastAPI
from app.db.session import engine, Base
from app.api import users, portfolio, positio, stocks, stocks_price, token, transactions
from app.db.session import SessionLocal
from app.services.stock_service import fetch_and_store_stocks
from app.services.stock_price_service import fetch_and_store_stock_price
from datetime import date
from app.core.errors.errorhandler import app_error_handler, generic_exception_handler
from app.core.errors.exceptions import AppError
from fastapi.middleware.cors import CORSMiddleware
from app.models.stock import Stock

origins = [
    "https://localhost:3000"
]


app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']

)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

Base.metadata.create_all(bind=engine)

app.include_router(stocks.router)
app.include_router(positio.router)
app.include_router(users.router)
app.include_router(portfolio.router)
app.include_router(stocks_price.router)
app.include_router(token.router)   
app.include_router(transactions.router)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    db = SessionLocal()
    try:
        if not db.query(Stock).first():
            fetch_and_store_stocks(db)
            fetch_and_store_stock_price(db)
            print("Database initialized with stock data.")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Investing Copilot API"}
