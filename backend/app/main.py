from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1.api import api_router as api_v1_router
from app.db.session import SessionLocal
from app.services.stocks.dependencies import build_stock_price_sync_service, build_stock_sync_service
from app.core.errors.errorhandler import app_error_handler, generic_exception_handler
from app.core.errors.exceptions import AppError
from fastapi.middleware.cors import CORSMiddleware
from app.models.stock import Stock
from app.json.ticker_map import load_ticker_map


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

app.include_router(api_v1_router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        if not db.query(Stock).first():
            ticker_map = load_ticker_map()
            stock_sync = build_stock_sync_service(db)
            stock_price_sync = build_stock_price_sync_service(db)
            stock_sync.sync_from_mapping(ticker_map)
            stock_price_sync.sync_all()
            
            print("Database initialized with stock data.")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Investing Copilot API"}
