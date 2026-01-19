from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.base_class import Base

DATABASE_URL = "postgresql+psycopg://myapp_user:myapp_password@localhost:5433/myapp_dev"


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models for metadata registration
import app.db.base  # noqa: E402,F401
