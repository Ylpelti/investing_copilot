import jwt
import pytest

from app.core.config import settings
from app.models import User
from app.security.hashing import hash_password


@pytest.fixture(scope="function")
def setup_user(test_db):
    password = "correct_password"
    user = User(
        username="authuser",
        email="authuser@example.com",
        pw_hash=hash_password(password),
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return {"user": user, "password": password}


def test_login_success(client, setup_user):
    response = client.post(
        "/api/v1/token",
        data={"username": setup_user["user"].username, "password": setup_user["password"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]
    assert body["expires_in"] > 0


def test_login_invalid_password(client, setup_user):
    response = client.post(
        "/api/v1/token",
        data={"username": setup_user["user"].username, "password": "wrong_password"},
    )
    assert response.status_code == 400
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    response = client.post("/api/v1/token", data={"username": "ghost", "password": "irrelevant"})
    assert response.status_code == 400
    assert "incorrect" in response.json()["detail"].lower()


def test_login_missing_fields(client):
    response = client.post("/api/v1/token", data={"username": "user"})
    assert response.status_code == 422


def test_login_returns_valid_jwt_format(client, setup_user):
    response = client.post(
        "/api/v1/token",
        data={"username": setup_user["user"].username, "password": setup_user["password"]},
    )
    token = response.json()["access_token"]
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload["sub"] == str(setup_user["user"].id)
    assert payload["type"] == "access"
    assert "exp" in payload
