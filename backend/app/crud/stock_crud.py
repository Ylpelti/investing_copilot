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

    def add(self, stock:Stock) -> None:
        self.db.add(stock)

    def get_by_ticker(self, ticker:str) -> Stock | None:
        return self.db.query(Stock).filter(Stock.ticker == ticker).first()
    
    def get_by_isin(self, isin:str) -> Stock | None:
        return self.db.query(Stock).filter(Stock.isin == isin).first()
    
    def get_by_id(self, id: int) -> Stock | None:
        return self.db.query(Stock).filter(Stock.id == id).first()
    
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
           

    
    
        

