import uuid
from datetime import date, datetime

from sqlmodel import SQLModel


class CycleEntryCreate(SQLModel):
    start_date: date
    end_date: date | None = None
    notes: str | None = None


class CycleEntryRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    start_date: date
    end_date: date | None
    cycle_length: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class CycleEntryUpdate(SQLModel):
    start_date: date | None = None
    end_date: date | None = None
    cycle_length: int | None = None
    notes: str | None = None
