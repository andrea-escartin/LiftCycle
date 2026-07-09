import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.auth.dependencies import get_current_user
from app.cycles.schemas import CycleCreate, CycleCreateResponse, CycleRead, CycleUpdate, PhaseResult
from app.cycles.service import (
    create_cycle,
    delete_cycle,
    get_current_phase,
    get_cycle,
    get_cycles,
    update_cycle,
)
from app.database import get_session
from app.users.models import User

router = APIRouter()


@router.post("/", response_model=CycleCreateResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: CycleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CycleCreateResponse:
    entry, warning = create_cycle(session, current_user.id, data)
    return CycleCreateResponse(**CycleRead.model_validate(entry).model_dump(), missed_period_warning=warning)


@router.get("/", response_model=list[CycleRead])
def list_cycles(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[CycleRead]:
    return get_cycles(session, current_user.id, skip, limit)


@router.get("/phase/current", response_model=PhaseResult)
def read_current_phase(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> PhaseResult:
    return get_current_phase(session, current_user.id)


@router.get("/{cycle_id}", response_model=CycleRead)
def read_cycle(
    cycle_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CycleRead:
    return get_cycle(session, current_user.id, cycle_id)


@router.patch("/{cycle_id}", response_model=CycleRead)
def patch_cycle(
    cycle_id: uuid.UUID,
    data: CycleUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CycleRead:
    return update_cycle(session, current_user.id, cycle_id, data)


@router.delete("/{cycle_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def remove_cycle(
    cycle_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    delete_cycle(session, current_user.id, cycle_id)
