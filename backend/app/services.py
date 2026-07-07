from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import CycleEntry, CycleEntryCreate, CycleEntryUpdate


def create_cycle(session: Session, user_id: int, data: CycleEntryCreate) -> CycleEntry:
    entry = CycleEntry(user_id=user_id, **data.model_dump())
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def get_cycles(
    session: Session, user_id: int, skip: int = 0, limit: int = 20
) -> list[CycleEntry]:
    return list(
        session.exec(
            select(CycleEntry)
            .where(CycleEntry.user_id == user_id)
            .order_by(CycleEntry.start_date.desc())
            .offset(skip)
            .limit(limit)
        ).all()
    )


def _get_or_404(session: Session, user_id: int, cycle_id: int) -> CycleEntry:
    entry = session.exec(
        select(CycleEntry).where(
            CycleEntry.id == cycle_id, CycleEntry.user_id == user_id
        )
    ).first()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cycle entry not found")
    return entry


def get_cycle(session: Session, user_id: int, cycle_id: int) -> CycleEntry:
    return _get_or_404(session, user_id, cycle_id)


def update_cycle(
    session: Session, user_id: int, cycle_id: int, data: CycleEntryUpdate
) -> CycleEntry:
    entry = _get_or_404(session, user_id, cycle_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(entry, field, value)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def delete_cycle(session: Session, user_id: int, cycle_id: int) -> None:
    entry = _get_or_404(session, user_id, cycle_id)
    session.delete(entry)
    session.commit()
