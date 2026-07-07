import uuid
from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    password: str
    last_period_start: date
    cycle_length_override: Optional[int] = None


class UserRead(SQLModel):
    id: uuid.UUID
    email: str
    unit_preference: str
    cycle_length_override: Optional[int]
    last_period_start: Optional[date]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    unit_preference: Optional[str] = None
    cycle_length_override: Optional[int] = None
