from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.cycles.models import CycleEntry
from app.cycles.schemas import Phase
from app.cycles.service import infer_phase
from app.users.models import User

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


# --- Phase inference (pure unit tests) ---


def _make_user(cycle_length_override: int | None = None) -> User:
    return User(email="phase@example.com", hashed_password="h", cycle_length_override=cycle_length_override)


def _make_cycle(user_id, start: date, end: date | None = None) -> CycleEntry:
    return CycleEntry(user_id=user_id, start_date=start, end_date=end)


def test_infer_phase_no_cycles_returns_unknown():
    user = _make_user()
    result = infer_phase(date(2024, 1, 1), [], user)
    assert result.phase == Phase.UNKNOWN
    assert result.days_into_cycle == 0
    assert result.cycle_length == 0


def test_infer_phase_default_cycle_length_phases():
    user = _make_user()
    start = date(2024, 1, 1)
    cycles = [_make_cycle(user.id, start)]

    assert infer_phase(start, cycles, user).phase == Phase.MENSTRUAL
    assert infer_phase(start + timedelta(days=4), cycles, user).phase == Phase.MENSTRUAL
    assert infer_phase(start + timedelta(days=5), cycles, user).phase == Phase.FOLLICULAR
    assert infer_phase(start + timedelta(days=13), cycles, user).phase == Phase.OVULATORY
    assert infer_phase(start + timedelta(days=14), cycles, user).phase == Phase.OVULATORY
    assert infer_phase(start + timedelta(days=15), cycles, user).phase == Phase.LUTEAL


def test_infer_phase_uses_override_when_fewer_than_three_complete_cycles():
    user = _make_user(cycle_length_override=24)
    start = date(2024, 1, 1)
    cycles = [_make_cycle(user.id, start)]

    result = infer_phase(start + timedelta(days=9), cycles, user)
    assert result.cycle_length == 24
    assert result.phase == Phase.OVULATORY

    result_luteal = infer_phase(start + timedelta(days=11), cycles, user)
    assert result_luteal.phase == Phase.LUTEAL


def test_infer_phase_uses_rolling_average_of_last_three_complete_cycles():
    user = _make_user()
    c0_start = date(2024, 1, 1)
    c1_start = c0_start + timedelta(days=100)  # outlier gap, must be excluded from the average
    c2_start = c1_start + timedelta(days=30)
    c3_start = c2_start + timedelta(days=28)
    c4_start = c3_start + timedelta(days=26)

    cycles = [
        _make_cycle(user.id, c0_start),
        _make_cycle(user.id, c1_start),
        _make_cycle(user.id, c2_start),
        _make_cycle(user.id, c3_start),
        _make_cycle(user.id, c4_start),
    ]

    result = infer_phase(c4_start, cycles, user)
    assert result.cycle_length == 28
    assert result.phase == Phase.MENSTRUAL


def test_infer_phase_respects_explicit_end_date_for_menstrual_offset():
    user = _make_user()
    start = date(2024, 1, 1)
    end = start + timedelta(days=6)
    cycles = [_make_cycle(user.id, start, end)]

    assert infer_phase(start + timedelta(days=6), cycles, user).phase == Phase.MENSTRUAL
    assert infer_phase(start + timedelta(days=7), cycles, user).phase == Phase.FOLLICULAR


# --- Current phase endpoint ---


def test_current_phase_unknown_with_no_cycles(client):
    _login(client)
    resp = client.get("/api/v1/cycles/phase/current")
    assert resp.status_code == 200
    assert resp.json()["phase"] == "UNKNOWN"


def test_current_phase_menstrual(client):
    _login(client)
    start = (date.today() - timedelta(days=2)).isoformat()
    client.post("/api/v1/cycles/", json={"start_date": start})
    resp = client.get("/api/v1/cycles/phase/current")
    assert resp.status_code == 200
    data = resp.json()
    assert data["phase"] == "MENSTRUAL"
    assert data["days_into_cycle"] == 2
    assert data["cycle_length"] == 28


def test_current_phase_requires_auth(client):
    resp = client.get("/api/v1/cycles/phase/current")
    assert resp.status_code == 401


# --- Missed period warning on create ---


def test_create_cycle_missed_period_warning(client):
    _login(client)
    old_start = (date.today() - timedelta(days=50)).isoformat()
    client.post("/api/v1/cycles/", json={"start_date": old_start})
    resp = client.post("/api/v1/cycles/", json={"start_date": date.today().isoformat()})
    assert resp.status_code == 201
    assert resp.json()["missed_period_warning"] is True


def test_create_cycle_no_missed_period_warning(client):
    _login(client)
    resp = client.post("/api/v1/cycles/", json={"start_date": date.today().isoformat()})
    assert resp.status_code == 201
    assert resp.json()["missed_period_warning"] is False
