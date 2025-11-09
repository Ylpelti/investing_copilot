import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security.hashing import hash_password
from app.db.session import SessionLocal, engine
from app.db.base_class import Base
from app.models import User

client = TestClient(app)

@pytest.fixture(autouse=True, scope="function")
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def setup_user(test_db):
    """Create a valid test user with a known password."""
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


class TestTokenAPI:
    def test_login_success(self, setup_user):
        """Ensure valid credentials return a JWT token."""
        data = {
            "username": setup_user["user"].username,
            "password": setup_user["password"],
        }
        response = client.post("/token", data=data)
        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert "token_type" in body
        assert body["token_type"] == "bearer"
        assert isinstance(body["access_token"], str)
        assert body["access_token"] != ""

    def test_login_invalid_password(self, setup_user):
        """Invalid password should return 400."""
        data = {
            "username": setup_user["user"].username,
            "password": "wrong_password",
        }
        response = client.post("/token", data=data)
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self):
        """Non-existent username should return 400."""
        data = {"username": "ghost", "password": "irrelevant"}
        response = client.post("/token", data=data)
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_missing_fields(self):
        """Missing form data should trigger validation error."""
        response = client.post("/token", data={"username": "user"})  # no password
        assert response.status_code == 422

    def test_login_returns_valid_jwt_format(self, setup_user):
        """Returned access_token should be decodable JWT."""
        import jwt
        from app.security.auth import SECRET_KEY, ALGORITHM

        data = {
            "username": setup_user["user"].username,
            "password": setup_user["password"],
        }
        response = client.post("/token", data=data)
        token = response.json()["access_token"]

        # Decode to verify structure and `sub` field
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == setup_user["user"].username
        assert "exp" in payload
