
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from typing import Optional

class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    buy_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolios.id"), nullable=False)
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="positions")

    stock_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=True)
    stock: Mapped[Optional["Stock"]] = relationship("Stock", back_populates="positions")

        