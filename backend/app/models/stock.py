from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from typing import Optional
from datetime import datetime

class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    isin: Mapped[Optional[str]] = mapped_column(String, unique=False, index=True, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    close_price: Mapped[Optional[float]] = mapped_column(Float, nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String, nullable=True)


    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True)
    

    positions: Mapped[list["Position"]] = relationship("Position", back_populates="stock")
    prices: Mapped[list["StockPrice"]] = relationship("StockPrice", back_populates="stock")

    def __repr__(self):
        return f"<Stock {self.ticker} ({self.name or " "})>"