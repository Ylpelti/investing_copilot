from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.portfolio import Portfolio



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    pw_hash: Mapped[str] = mapped_column(String, nullable=False)

    #created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    #updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), on_update=func.now())

    portfolios: Mapped[list["Portfolio"]] = relationship("Portfolio", back_populates="user")



