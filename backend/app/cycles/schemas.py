import uuid
from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel


class CycleEntryCreate(SQLModel):
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None


class CycleEntryRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    start_date: date
    end_date: Optional[date]
    cycle_length: Optional[int]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class CycleEntryUpdate(SQLModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    cycle_length: Optional[int] = None
    notes: Optional[str] = None
