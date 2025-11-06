from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.security.hashing import hash_password
from app.core.errors.exceptions import UsernameDuplicateError, EmailDuplicateError
from app.crud.base_crud import BaseCrud

class UserCrud(BaseCrud[User]):
    model = User
    def get_user_by_email(self, email:str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate) -> User:

        if self.get_user_by_username(user.username):
            raise UsernameDuplicateError()
        if self.get_user_by_email(user.email):
            raise EmailDuplicateError()
        db_user = User(
            username = user.username,
            email = user.email,
            pw_hash = hash_password(user.password)

        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user



    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()