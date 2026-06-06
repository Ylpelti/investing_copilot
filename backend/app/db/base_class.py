from sqlalchemy.orm import declarative_base, DeclarativeBase

# Shared declarative base for all SQLAlchemy models
class Base(DeclarativeBase):
    pass

__all__ = ["Base"]
