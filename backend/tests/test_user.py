import pytest
from pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError

from app import models
from app.crud.user_crud import UserCrud
from app.schemas.user import UserCreate


def test_users_unique_username(test_db, test_user):
    duplicate = models.User(
        username=test_user.username,
        email="testuser2@example.com",
        pw_hash="plain_hash",
    )
    test_db.add(duplicate)
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()


def test_create_user_success(test_db):
    crud = UserCrud(test_db)
    created = crud.create_user(
        UserCreate(
            username="testuser2",
            email="testuser2@gmail.com",
            password="salainen123",
        )
    )
    assert created.username == "testuser2"
    assert created.email == "testuser2@gmail.com"
    assert created.pw_hash != "salainen123"


def test_get_user_by_id(test_db):
    crud = UserCrud(test_db)
    created = crud.create_user(
        UserCreate(username="charlie", email="charlie@example.com", password="topsecret")
    )
    fetched = crud.get_id_or_404(created.id)
    assert fetched.username == "charlie"
    assert fetched.email == "charlie@example.com"


def test_user_schema_too_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="shortpassworduser",
            email="shortpassworduser@example.com",
            password="short",
        )


def test_create_user_api_success(client):
    response = client.post(
        "/api/v1/users",
        json={
            "username": "apiuser",
            "email": "apiuser@example.com",
            "password": "validpassword123",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "apiuser"
    assert body["email"] == "apiuser@example.com"
    assert "id" in body


def test_create_user_invalid_email(client):
    response = client.post(
        "/api/v1/users",
        json={
            "username": "invalidemailuser",
            "email": "invalidemail",
            "password": "validpassword123",
        },
    )
    assert response.status_code == 422


def test_read_current_user_me(client, auth_headers, test_user):
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == test_user.id
    assert body["username"] == test_user.username


def test_read_user_by_id_route_returns_authenticated_user(client, auth_headers, test_user):
    response = client.get(f"/api/v1/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == test_user.id
