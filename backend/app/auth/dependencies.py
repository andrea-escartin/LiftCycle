import uuid

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
from sqlmodel import Session

from app.auth.service import verify_token
from app.config import settings
from app.database import get_session
from app.users.models import User

_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User:
    token = request.cookies.get("access_token")
    if token is None:
        raise _credentials_exception
    try:
        payload = verify_token(token, settings.SECRET_KEY)
        sub = payload.get("sub")
        if sub is None:
            raise _credentials_exception
        user_id = uuid.UUID(sub)
    except (JWTError, ValueError):
        raise _credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
