from fastapi.testclient import TestClient
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..dependencies import get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

Path("./test.db").unlink(missing_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_db(request):
    response = client.post(
        "/users/",
        json={"email": "alan@example.com", "password": "password"},
    )


def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]


def test_login():
    response = client.post(
        "/token",
        data={"username": "alan@example.com", "password": "password"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    assert data["token_type"] == "bearer"
    assert type(data["access_token"]) is str


def test_get_users():
    response = client.post(
        "/token",
        data={"username": "alan@example.com", "password": "password"},
    )
    data = response.json()

    response = client.get(
        "/users/",
        headers={"Authorization": "Bearer " + data["access_token"]}
    )
    assert response.status_code == 200, response.text
    data = [u for u in response.json() if u["email"] == "alan@example.com"]
    assert len(data) == 1
