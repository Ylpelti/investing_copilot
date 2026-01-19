from sqlalchemy import Integer, Numeric, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
from datetime import date as DateType
from typing import TYPE_CHECKING
from decimal import Decimal


if TYPE_CHECKING:
    from app.models.stock import Stock


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    date: Mapped[DateType] = mapped_column(Date, nullable=False)
    open_price: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=True)
    high_price: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=True)
    low_price: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=True)
    close_price: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=True)

    stock: Mapped["Stock"] = relationship("Stock", back_populates="prices")

    def __repr__(self):
        return f"<StockPrice stock_id={self.stock_id}, date={self.date}, close={self.close_price}>"
