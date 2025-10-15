from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import pandas as pd
from app.models.portfolio import Portfolio
from app.models.stock_price import StockPrice


def calculate_portfolio_value(db: Session, portfolio_id: int) -> float | None:
    portfolio = get_portfolio(db, portfolio_id)
    if not portfolio:
        return None
    for pos in portfolio.positions:
        print(f"Position ID: {pos.id}, Stock Ticker: {pos.stock.ticker}, Quantity: {pos.quantity}")
    total_value = sum(pos.quantity * pos.stock.close_price for pos in portfolio.positions)
    return total_value

 

def stock_returns(db:Session, stock_id: int):
    stock_data = db.query(StockPrice).filter(StockPrice.stock_id == stock_id).order_by(StockPrice.id).all()
    if len(stock_data) < 2:
        return None
    returns = (stock_data[-1].close_price - stock_data[0].close_price) / stock_data[0].close_price
    return returns
        
def stock_returns_amount(db:Session, stock_id: int):
    stock_data = db.query(StockPrice).filter(StockPrice.stock_id == stock_id).order_by(StockPrice.id).all()
    if len(stock_data) < 2:
        return None
    profit = stock_data[-1].close_price - stock_data[0].close_price
    return profit

def get_portfolio(db:Session, portfolio_id:int):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    return portfolio


    