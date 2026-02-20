from sqlalchemy import Numeric, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
from typing import Optional
from datetime import datetime
from typing import TYPE_CHECKING
from decimal import Decimal


if TYPE_CHECKING:
    from app.models.portfolio import Portfolio
    from app.models.stock import Stock

class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("portfolio_id", "stock_id", name="uq_portfolio_symbol"),)


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    buy_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 6), nullable=True)

    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="positions")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)
        
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True)

    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    stock: Mapped[Optional["Stock"]] = relationship("Stock", back_populates="positions")

    def __repr__(self):
        return f"<Position id={self.id}, portfolio={self.portfolio_id}, qty={self.quantity}>"
