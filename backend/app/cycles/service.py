import uuid
from datetime import date, datetime

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.cycles.models import CycleEntry
from app.cycles.schemas import CycleCreate, CycleUpdate, Phase, PhaseResult
from app.users.models import User


def _compute_cycle_length(cycles: list[CycleEntry], user: User) -> int:
    sorted_cycles = sorted(cycles, key=lambda c: c.start_date)
    completed_lengths = [
        (sorted_cycles[i + 1].start_date - sorted_cycles[i].start_date).days for i in range(len(sorted_cycles) - 1)
    ]
    if len(completed_lengths) >= 3:
        last_three = completed_lengths[-3:]
        return round(sum(last_three) / len(last_three))
    if user.cycle_length_override:
        return user.cycle_length_override
    return 28


def infer_phase(target_date: date, cycles: list[CycleEntry], user: User) -> PhaseResult:
    past_cycles = [c for c in cycles if c.start_date <= target_date]
    if not past_cycles:
        return PhaseResult(phase=Phase.UNKNOWN, days_into_cycle=0, cycle_length=0)

    current_cycle = max(past_cycles, key=lambda c: c.start_date)
    cycle_length = _compute_cycle_length(cycles, user)
    days_into_cycle = (target_date - current_cycle.start_date).days

    if current_cycle.end_date:
        menstrual_end_offset = (current_cycle.end_date - current_cycle.start_date).days
    else:
        menstrual_end_offset = 4

    estimated_ovulation_day = cycle_length - 14

    if days_into_cycle <= menstrual_end_offset:
        phase = Phase.MENSTRUAL
    elif days_into_cycle < estimated_ovulation_day - 1:
        phase = Phase.FOLLICULAR
    elif estimated_ovulation_day - 1 <= days_into_cycle <= estimated_ovulation_day:
        phase = Phase.OVULATORY
    else:
        phase = Phase.LUTEAL

    return PhaseResult(phase=phase, days_into_cycle=days_into_cycle, cycle_length=cycle_length)


def _get_all_cycles(session: Session, user_id: uuid.UUID) -> list[CycleEntry]:
    return list(session.exec(select(CycleEntry).where(CycleEntry.user_id == user_id)).all())


def create_cycle(session: Session, user_id: uuid.UUID, data: CycleCreate) -> tuple[CycleEntry, bool]:
    user = session.get(User, user_id)
    existing_cycles = _get_all_cycles(session, user_id)

    warning = False
    if existing_cycles:
        last_cycle = max(existing_cycles, key=lambda c: c.start_date)
        cycle_length = _compute_cycle_length(existing_cycles, user)
        if (date.today() - last_cycle.start_date).days > cycle_length * 1.5:
            warning = True

    entry = CycleEntry(user_id=user_id, **data.model_dump())
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry, warning


def get_cycles(session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> list[CycleEntry]:
    return list(
        session.exec(
            select(CycleEntry)
            .where(CycleEntry.user_id == user_id)
            .order_by(CycleEntry.start_date.desc())
            .offset(skip)
            .limit(limit)
        ).all()
    )


def _get_or_404(session: Session, user_id: uuid.UUID, cycle_id: uuid.UUID) -> CycleEntry:
    entry = session.exec(select(CycleEntry).where(CycleEntry.id == cycle_id, CycleEntry.user_id == user_id)).first()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cycle entry not found")
    return entry


def get_cycle(session: Session, user_id: uuid.UUID, cycle_id: uuid.UUID) -> CycleEntry:
    return _get_or_404(session, user_id, cycle_id)


def update_cycle(session: Session, user_id: uuid.UUID, cycle_id: uuid.UUID, data: CycleUpdate) -> CycleEntry:
    entry = _get_or_404(session, user_id, cycle_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(entry, field, value)
    entry.updated_at = datetime.utcnow()
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def delete_cycle(session: Session, user_id: uuid.UUID, cycle_id: uuid.UUID) -> None:
    entry = _get_or_404(session, user_id, cycle_id)
    session.delete(entry)
    session.commit()


def get_current_phase(session: Session, user_id: uuid.UUID) -> PhaseResult:
    user = session.get(User, user_id)
    cycles = _get_all_cycles(session, user_id)
    return infer_phase(date.today(), cycles, user)
