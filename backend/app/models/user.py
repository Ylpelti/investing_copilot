from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    pw_hash: Mapped[str] = mapped_column(String, nullable=False)
    portfolios: Mapped[list["Portfolio"]] = relationship("Portfolio", back_populates="user")




