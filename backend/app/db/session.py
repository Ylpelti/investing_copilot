from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.base_class import Base
from app.core.config import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models for metadata registration
import app.db.base  # noqa: E402,F401
