
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
from typing import Optional
from datetime import datetime

class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("portfolio_id", "symbol", name="uq_portfolio_symbol"),)


    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    buy_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolios.id"), nullable=False, index=True)
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="positions", cascade="all, delete")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)
        
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False)

    stock_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=True, index=True)
    stock: Mapped[Optional["Stock"]] = relationship("Stock", back_populates="positions")

    def __repr__(self):
        return f"<Position id={self.id}, portfolio={self.portfolio_id}, symbol={self.symbol}, qty={self.quantity}>"
