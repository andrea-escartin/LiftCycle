from datetime import date, datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class CycleEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    start_date: date
    end_date: Optional[date] = None
    cycle_length: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    email: str
    created_at: datetime


class CycleEntryCreate(SQLModel):
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None


class CycleEntryRead(SQLModel):
    id: int
    user_id: int
    start_date: date
    end_date: Optional[date]
    cycle_length: Optional[int]
    notes: Optional[str]
    created_at: datetime


class CycleEntryUpdate(SQLModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    cycle_length: Optional[int] = None
    notes: Optional[str] = None
