import pandas as pd
from typing import IO, BinaryIO
from app.crud.transaction_crud import TransactionCrud
from app.schemas.transactions import TransactionCreate
from app.crud.stock_crud import StockCrud
from app.core.errors.exceptions import NotFound
from datetime import datetime
from decimal import Decimal
from app.models.transaction import TransactionType
from app.infrastructure.parsers.base_parser import BaseParser
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.stocks.stock_service import StockService
from app.dto.transaction_dto import NormalizedTransactionDTO



class PortfolioImportService:
    def __init__(self, tx_repo, portfolio_service: PortfolioService, stock_service: StockService, current_user_id, parser: BaseParser):
        self.tx_repo = tx_repo
        self.portfolio_service = portfolio_service
        self.stock_service = stock_service
        self.current_user_id = current_user_id
        self.parser = parser

    def import_csv(self, file: BinaryIO, portfolio_id: int):
        self.portfolio_service.get_owned_portfolio_or_404(portfolio_id)
        dtos = self.parser.parse(file)
        return self.normalize_transactionCreate(dtos, portfolio_id)

    def normalize_transactionCreate(self, dtos: list[NormalizedTransactionDTO], portfolio_id: int):
        result = []
        for dto in dtos:
            stock = self.stock_service.get_stock_by_isin(dto.isin)
            tx = TransactionCreate(
                portfolio_id=portfolio_id,
                stock_id=stock.id, #type: ignore
                type = TransactionType.BUY,
                quantity=dto.quantity,
                price = dto.buy_price,
                timestamp=dto.date
            )
            result.append(tx)
        return result
    
    



    
        

def normalize_transaction(isin:str, quantity: Decimal, buy_price: Decimal, trade_date:datetime, db, portfolio_id):
    crud = StockCrud(db)
    stock = crud.get_stock_by_isin(isin)
    if not stock:
        raise NotFound(message="Stock not found with that isin")
        
    
    return TransactionCreate(
         portfolio_id=portfolio_id,
         stock_id=stock.id,
         type=TransactionType.BUY,
         quantity=quantity,
         price=buy_price,
         timestamp=trade_date       
    )