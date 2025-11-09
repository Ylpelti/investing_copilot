from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.base_class import Base

DATABASE_URL = "sqlite:///./investing_copilot.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models for metadata registration
import app.db.base  # noqa: E402,F401
