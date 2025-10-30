import pytest
from app.schemas.user import UserBase
from app import models
from sqlalchemy.exc import IntegrityError
from app.crud.user_crud import UserCrud
from app.schemas.user import UserCreate

def test_users_unqie_username(test_db, test_user):
    user = models.User(
        username="testuser", email="testuser2@example.com", pw_hash="salainen1234"
    )
    test_db.add(user)
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()

def test_create_user(test_db):
    user = models.User(
        username="testuser2",
        email = "testuser2@gmail.com",
        pw_hash = "salainen123"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

def test_user_by_id(test_db):
    crud = UserCrud(test_db)
    user_data = UserCreate(username="charlie", email="charlie@example.com", password="topsecret")
    new_user = crud.create_user(user_data)

    fetched_user = crud.get_id_or_404(new_user.id)

    assert fetched_user.username == 'charlie'
    assert fetched_user.email == "charlie@example.com"
