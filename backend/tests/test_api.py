from fastapi.testclient import TestClient

_NONEXISTENT_UUID = "00000000-0000-0000-0000-000000000000"


def _login(client: TestClient, email: str = "test@example.com", password: str = "testpass") -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "last_period_start": "2024-01-01"},
    )
    client.post("/api/v1/auth/login", data={"username": email, "password": password})


# --- Auth ---

def test_register_new_user(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "new@example.com", "password": "pw", "last_period_start": "2024-01-01"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "pw", "last_period_start": "2024-01-01"},
    )
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "other", "last_period_start": "2024-01-01"},
    )
    assert resp.status_code == 400


def test_login_correct_credentials(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "secret", "last_period_start": "2024-01-01"},
    )
    resp = client.post("/api/v1/auth/login", data={"username": "user@example.com", "password": "secret"})
    assert resp.status_code == 200
    assert "access_token" in resp.cookies


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "secret", "last_period_start": "2024-01-01"},
    )
    resp = client.post("/api/v1/auth/login", data={"username": "user@example.com", "password": "wrong"})
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post("/api/v1/auth/login", data={"username": "nobody@example.com", "password": "pw"})
    assert resp.status_code == 401


def test_refresh_token(client):
    _login(client)
    resp = client.post("/api/v1/auth/refresh")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
    assert "access_token" in resp.cookies


def test_logout(client):
    _login(client)
    resp = client.post("/api/v1/auth/logout")
    assert resp.status_code == 200
    resp = client.get("/api/v1/cycles/")
    assert resp.status_code == 401


# --- Cycles ---

def test_create_cycle(client):
    _login(client)
    resp = client.post("/api/v1/cycles/", json={"start_date": "2024-01-15"})
    assert resp.status_code == 201
    assert resp.json()["start_date"] == "2024-01-15"


def test_get_cycles_list(client):
    _login(client)
    client.post("/api/v1/cycles/", json={"start_date": "2024-01-15"})
    resp = client.get("/api/v1/cycles/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["start_date"] == "2024-01-15"


def test_get_cycle_by_id(client):
    _login(client)
    created = client.post("/api/v1/cycles/", json={"start_date": "2024-02-01"}).json()
    resp = client.get(f"/api/v1/cycles/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_cycle_wrong_id(client):
    _login(client)
    resp = client.get(f"/api/v1/cycles/{_NONEXISTENT_UUID}")
    assert resp.status_code == 404


def test_patch_cycle(client):
    _login(client)
    created = client.post("/api/v1/cycles/", json={"start_date": "2024-03-01"}).json()
    resp = client.patch(f"/api/v1/cycles/{created['id']}", json={"notes": "updated note"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["notes"] == "updated note"
    assert data["start_date"] == "2024-03-01"


def test_delete_cycle(client):
    _login(client)
    created = client.post("/api/v1/cycles/", json={"start_date": "2024-04-01"}).json()
    resp = client.delete(f"/api/v1/cycles/{created['id']}")
    assert resp.status_code == 204


def test_get_deleted_cycle(client):
    _login(client)
    created = client.post("/api/v1/cycles/", json={"start_date": "2024-05-01"}).json()
    client.delete(f"/api/v1/cycles/{created['id']}")
    resp = client.get(f"/api/v1/cycles/{created['id']}")
    assert resp.status_code == 404


def test_no_token_returns_401(client):
    resp = client.get("/api/v1/cycles/")
    assert resp.status_code == 401
