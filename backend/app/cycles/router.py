import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.auth.dependencies import get_current_user
from app.cycles.schemas import CycleEntryCreate, CycleEntryRead, CycleEntryUpdate
from app.cycles.service import create_cycle, delete_cycle, get_cycle, get_cycles, update_cycle
from app.database import get_session
from app.users.models import User

router = APIRouter()


@router.post("/", response_model=CycleEntryRead, status_code=status.HTTP_201_CREATED)
def create(
    data: CycleEntryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CycleEntryRead:
    return create_cycle(session, current_user.id, data)


@router.get("/", response_model=list[CycleEntryRead])
def list_cycles(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[CycleEntryRead]:
    return get_cycles(session, current_user.id, skip, limit)


@router.get("/{cycle_id}", response_model=CycleEntryRead)
def read_cycle(
    cycle_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CycleEntryRead:
    return get_cycle(session, current_user.id, cycle_id)


@router.patch("/{cycle_id}", response_model=CycleEntryRead)
def patch_cycle(
    cycle_id: uuid.UUID,
    data: CycleEntryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CycleEntryRead:
    return update_cycle(session, current_user.id, cycle_id, data)


@router.delete("/{cycle_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def remove_cycle(
    cycle_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    delete_cycle(session, current_user.id, cycle_id)
