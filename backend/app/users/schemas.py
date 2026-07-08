import uuid
from datetime import date, datetime

from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    password: str
    last_period_start: date
    cycle_length_override: int | None = None


class UserRead(SQLModel):
    id: uuid.UUID
    email: str
    unit_preference: str
    cycle_length_override: int | None
    last_period_start: date | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None
    unit_preference: str | None = None
    cycle_length_override: int | None = None
