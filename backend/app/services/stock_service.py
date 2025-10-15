import yfinance as yf
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.stock import StockCreate
from app.crud import stock_crud

Helsinki_Tickers = [
    "NOKIA.HE", "KEMIRA.HE",  "WRT1V.HE",
    "UPM.HE", "STERV.HE", "ORNBV.HE", "NESTE.HE", "RAIVV.HE",
    "ELISA.HE", "FORTUM.HE", "METSO.HE", "MANTA.HE",
    "TYRES.HE", "KCR.HE", "HUH1V.HE", "VALMET.HE", "TIETO.HE", "ORNBV.HE",
    "KESKOB.HE", "KOJAMO.HE", "SSABBH.HE", "STERV.HE", "NDA-FI.HE", "KOJAMO.HE"
]

def fetch_and_store_stocks(session: Session):
    for ticker in Helsinki_Tickers:
        try: 
            stock_data = yf.Ticker(ticker).info
        except:
            print('\ndid not fetch data for', ticker, '\n')
            continue
        if 'regularMarketPrice' in stock_data:
            stock = StockCreate(
                ticker=ticker,
                name=stock_data.get('shortName', ''),
                close_price=stock_data['regularMarketPrice'],
                updated_at=datetime.utcnow(),
                sector=stock_data.get('sector', '')
            )
            stock_crud.create_stock(session, stock)

