import uuid
from datetime import date, datetime
from enum import StrEnum

from sqlmodel import SQLModel


class Phase(StrEnum):
    MENSTRUAL = "MENSTRUAL"
    FOLLICULAR = "FOLLICULAR"
    OVULATORY = "OVULATORY"
    LUTEAL = "LUTEAL"
    UNKNOWN = "UNKNOWN"


class CycleCreate(SQLModel):
    start_date: date
    end_date: date | None = None
    notes: str | None = None


class CycleRead(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    start_date: date
    end_date: date | None
    cycle_length: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class CycleCreateResponse(CycleRead):
    missed_period_warning: bool


class CycleUpdate(SQLModel):
    start_date: date | None = None
    end_date: date | None = None
    cycle_length: int | None = None
    notes: str | None = None


class PhaseResult(SQLModel):
    phase: Phase
    days_into_cycle: int
    cycle_length: int
