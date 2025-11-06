from pydantic_core import ValidationError
import pytest
from app.schemas.user import UserBase
from app import models
from sqlalchemy.exc import IntegrityError
from app.crud.user_crud import UserCrud
from app.schemas.user import UserCreate
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_users_unqie_username(test_db, test_user):
    user = models.User(
        username="testuser", email="testuser2@example.com", pw_hash="salainen1234"
    )
    test_db.add(user)
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()

def test_create_user_success(test_db):
    crud = UserCrud(test_db)
    user = UserCreate(
        username="testuser2",
        email="testuser2@gmail.com",
        password="salainen123"
    )
    created = crud.create_user(user)
    assert created.username == "testuser2"
    assert created.email == "testuser2@gmail.com"
    assert created.pw_hash != "salainen123"

def test_user_by_id(test_db):
    crud = UserCrud(test_db)
    user_data = UserCreate(username="charlie", email="charlie@example.com", password="topsecret")
    new_user = crud.create_user(user_data)

    fetched_user = crud.get_id_or_404(new_user.id)

    assert fetched_user.username == 'charlie'
    assert fetched_user.email == "charlie@example.com"

def test_too_short_password(test_db):
    response = client.post("/users", json={
        "username": "shortpassworduser",
        "email": "shortpassworduser@example.com",
        "password": "short"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "password"]


def test_invalid_email_format(test_db):
    response = client.post("/users", json={
        "username": "invalidemailuser",
        "email": "invalidemail",
        "password": "validpassword123"
    })

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "email"]

def test_missing_username_field(test_db):
    response = client.post("/users", json={
        "email": "missingusername@example.com",
        "password": "validpassword123"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "username"]