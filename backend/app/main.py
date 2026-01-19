from fastapi import FastAPI
from app.db.session import engine, Base
from app.api import users, portfolio, positio, stocks, stocks_price, token
from app.db.session import SessionLocal
from app.services.stock_service import fetch_and_store_stocks
from app.services.stock_price_service import fetch_and_store_stock_price
from app.tasks.portfolio_analyysi import load_prices_df, get_positions_map, portfolio_value_series, build_dashboard_from_series
from datetime import date
from app.core.errors.errorhandler import app_error_handler, generic_exception_handler
from app.core.errors.exceptions import AppError
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://localhost:3000"
]


app = FastAPI()

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




@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    fetch_and_store_stocks(db)
    fetch_and_store_stock_price(db)
    
    

    db.close()
    print("Database initialized with stock data.")
    prices = load_prices_df(db, [1,2,6,8], start=date(2024,1,1), end=date(2025,12,31))
    
    pos_map = get_positions_map(db, 1)
    dashboard = build_dashboard_from_series(portfolio_value_series(db, 1, start=date(2025, 1, 1)))

    
    print('Position mapping', pos_map )
    print('Portfolio value: ', portfolio_value_series(db, 1, start=date(2025, 1, 1)).to_string())
    print("Sample price data load:", prices.to_string())
    print("Dashboard:", dashboard)
    




@app.get("/")
def read_root():
    return {"message": "Welcome to the Investing Copilot API"}
