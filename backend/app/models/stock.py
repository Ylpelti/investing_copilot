from sqlalchemy import Integer, String, Numeric, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
from typing import Optional
from datetime import datetime
from typing import TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from app.models.positio import Position
    from app.models.stock_price import StockPrice
    from app.models.transaction import PortfolioTransaction

class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    isin: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    close_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 6), nullable=True)
    sector: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True)
    
    positions: Mapped[list["Position"]] = relationship("Position", back_populates="stock")
    prices: Mapped[list["StockPrice"]] = relationship("StockPrice", back_populates="stock")
    transactions: Mapped[list["PortfolioTransaction"]] = relationship("PortfolioTransaction", back_populates="stock", lazy="noload")


    def __repr__(self):
        return f"<Stock {self.ticker} ({self.name or ''})>"
