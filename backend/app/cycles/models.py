import uuid
from datetime import date, datetime
from uuid import uuid4

from sqlmodel import Field, SQLModel


class CycleEntry(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    start_date: date
    end_date: date | None = None
    cycle_length: int | None = None
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
