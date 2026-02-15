from datetime import datetime, UTC
from app.crud.base_crud import BaseCrud
from app.models.stock import Stock
from app.schemas.stock import StockCreate
import logging
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from app.core.errors.exceptions import BadRequest, NotFound
from typing import Optional

logger = logging.getLogger(__name__)

class StockCrud(BaseCrud):
    model = Stock

    def create_stock(self, stock: StockCreate) -> Stock:
        existing = self.db.query(Stock).filter(Stock.ticker == stock.ticker).first()
        if existing:
            logger.info(f"Already stock {stock.ticker} in database")
            return existing
        db_stock = Stock(
        ticker=stock.ticker,
        name=stock.name,
        isin=stock.isin,
        close_price=stock.close_price,
        updated_at=stock.updated_at or datetime.now(UTC),
        sector=stock.sector,
    )
        try:
            self.db.add(db_stock)
            self.db.commit()
            self.db.refresh(db_stock)
            logger.info(f"Stock creater with ticker {db_stock.ticker}")
            return db_stock
        except IntegrityError as e:
            self.db.rollback()
            raise BadRequest(message="Failed to create stock — possible duplicate ticker.")
        
    def update_stock_price(self, ticker: str, new_price: float) -> Stock:
        stock = self.db.query(Stock).filter(Stock.ticker == ticker).first()
        if not stock:
            raise NotFound(message=f"Stock {ticker} not found.")

        stock.close_price = new_price
        stock.updated_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(stock)
        logger.info(f"Updated {ticker} price to {new_price}")
        return stock
    
    def get_stock_by_isin(self, isin: str) -> Optional[Stock]:
        stock = self.db.query(Stock).filter(Stock.isin == isin).first()
        if not stock:
            raise NotFound(message=f"Not found with isin: {isin}")
        return stock
    
    def get_stock_by_ticker(self, ticker:str) -> Optional[Stock]:
        stock = self.db.query(Stock).filter(Stock.ticker == ticker).first()
        if not stock:
            raise NotFound(message=f"Not found with ticker: {ticker}")
        return stock
    
    def list_or_search(
            self,
            q: str | None,
            limit: int,
            offset: int
    ) -> list[Stock]:
        query = self.db.query(Stock)

        if q:
            search_term = f"%{q}%"
            query = query.filter(
                or_(
                    Stock.ticker.ilike(search_term),
                    Stock.name.ilike(search_term)
                )
            )
        return (
            query
            .order_by(Stock.ticker.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
           
    
    def search_stock_by_ticker(self, query:str | None = None, limit: int = 5) -> list[Stock]:
        

        if not query:
            return []
        
        q = query.strip().upper()
        return (
            self.db.query(Stock)
            .filter(
                or_(
                Stock.ticker.ilike(f"{q}%"),
                Stock.name.ilike(f"{q}%")
                )
            )
            .order_by(Stock.ticker)
            .limit(limit)
            .all()
        )

    
    
        

