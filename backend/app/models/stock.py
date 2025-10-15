from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from typing import Optional
from datetime import datetime

class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(String, default=datetime.utcnow(), nullable=True)
    

    positions: Mapped[list["Position"]] = relationship("Position", back_populates="stock")
    prices: Mapped[list["StockPrice"]] = relationship("StockPrice", back_populates="stock")