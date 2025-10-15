from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.security.hashing import hash_password

def read_users(db: Session) -> list[User]:
    return db.query(User).all()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username = user.username,
        email = user.email,
        pw_hash = hash_password(user.password)

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()