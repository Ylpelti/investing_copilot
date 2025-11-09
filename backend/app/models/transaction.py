from enum import Enum as PyEnum
from sqlalchemy import Enum, Integer, Float, String, ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base_class import Base

class TransactionType(str, PyEnum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"

class PortfolioTransaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
    CheckConstraint("quantity >= 0", name="check_quantity_non_negative"),
    CheckConstraint("price >= 0", name="check_price_non_negative"),
)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False, index=True)

    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, name="transaction_type_enum"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    total_value: Mapped[float] = mapped_column(Float, nullable=False)
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="transactions")
    stock: Mapped["Stock"] = relationship("Stock", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction id={self.id}, type={self.type}, symbol={self.symbol}, qty={self.quantity}, price={self.price}>"
