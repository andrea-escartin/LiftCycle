from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth.service import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.config import settings
from app.database import get_session
from app.users.models import User
from app.users.schemas import UserCreate, UserRead

router = APIRouter()


def _set_auth_cookies(response: Response, user: User) -> None:
    secure = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="access_token",
        value=create_access_token({"sub": str(user.id)}),
        httponly=True,
        samesite="lax",
        path="/",
        secure=secure,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=create_refresh_token({"sub": str(user.id)}),
        httponly=True,
        samesite="lax",
        path="/",
        secure=secure,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, response: Response, session: Session = Depends(get_session)) -> User:
    existing = session.exec(select(User).where(User.email == body.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        last_period_start=body.last_period_start,
        cycle_length_override=body.cycle_length_override,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    _set_auth_cookies(response, user)
    return user


@router.post("/login", response_model=UserRead)
def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> User:
    user = session.exec(select(User).where(User.email == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    _set_auth_cookies(response, user)
    return user


@router.post("/refresh")
def refresh(request: Request, response: Response) -> dict[str, bool]:
    token = request.cookies.get("refresh_token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
    try:
        payload = verify_token(token, settings.REFRESH_SECRET_KEY)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    secure = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="access_token",
        value=create_access_token({"sub": payload["sub"]}),
        httponly=True,
        samesite="lax",
        path="/",
        secure=secure,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"ok": True}


@router.post("/logout")
def logout(response: Response) -> dict[str, bool]:
    response.delete_cookie(key="access_token", path="/", httponly=True, samesite="lax")
    response.delete_cookie(key="refresh_token", path="/", httponly=True, samesite="lax")
    return {"ok": True}
