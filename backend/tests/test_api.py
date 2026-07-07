from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.db import get_session
from app.main import app


@pytest.fixture(name="client")
def client_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override

    with patch("app.main.create_db_and_tables"):
        with TestClient(app) as client:
            yield client

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)


def _auth_headers(client: TestClient, email: str = "test@example.com", password: str = "testpass") -> dict:
    client.post("/auth/register", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# --- Auth ---

def test_register_new_user(client):
    resp = client.post("/auth/register", json={"email": "new@example.com", "password": "pw"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "pw"})
    resp = client.post("/auth/register", json={"email": "dup@example.com", "password": "other"})
    assert resp.status_code == 400


def test_login_correct_credentials(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "secret"})
    resp = client.post("/auth/login", data={"username": "user@example.com", "password": "secret"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "secret"})
    resp = client.post("/auth/login", data={"username": "user@example.com", "password": "wrong"})
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post("/auth/login", data={"username": "nobody@example.com", "password": "pw"})
    assert resp.status_code == 401


# --- Cycles ---

def test_create_cycle(client):
    headers = _auth_headers(client)
    resp = client.post("/cycles/", json={"start_date": "2024-01-15"}, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["start_date"] == "2024-01-15"


def test_get_cycles_list(client):
    headers = _auth_headers(client)
    client.post("/cycles/", json={"start_date": "2024-01-15"}, headers=headers)
    resp = client.get("/cycles/", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["start_date"] == "2024-01-15"


def test_get_cycle_by_id(client):
    headers = _auth_headers(client)
    created = client.post("/cycles/", json={"start_date": "2024-02-01"}, headers=headers).json()
    resp = client.get(f"/cycles/{created['id']}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_cycle_wrong_id(client):
    headers = _auth_headers(client)
    resp = client.get("/cycles/999", headers=headers)
    assert resp.status_code == 404


def test_patch_cycle(client):
    headers = _auth_headers(client)
    created = client.post("/cycles/", json={"start_date": "2024-03-01"}, headers=headers).json()
    resp = client.patch(f"/cycles/{created['id']}", json={"notes": "updated note"}, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["notes"] == "updated note"
    assert data["start_date"] == "2024-03-01"


def test_delete_cycle(client):
    headers = _auth_headers(client)
    created = client.post("/cycles/", json={"start_date": "2024-04-01"}, headers=headers).json()
    resp = client.delete(f"/cycles/{created['id']}", headers=headers)
    assert resp.status_code == 204


def test_get_deleted_cycle(client):
    headers = _auth_headers(client)
    created = client.post("/cycles/", json={"start_date": "2024-05-01"}, headers=headers).json()
    client.delete(f"/cycles/{created['id']}", headers=headers)
    resp = client.get(f"/cycles/{created['id']}", headers=headers)
    assert resp.status_code == 404


def test_no_token_returns_401(client):
    resp = client.get("/cycles/")
    assert resp.status_code == 401
