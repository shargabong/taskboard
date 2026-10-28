from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session

from app.db import get_session
from app.models import Role, User


def get_optional_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    user = session.get(User, user_id)
    if user is None or not user.is_active:
        request.session.clear()
        return None
    return user


def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User:
    user = get_optional_user(request, session)
    if user is None:
        next_url = request.url.path
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": f"/login?next={next_url}"},
        )
    return user


def require_roles(*roles: Role):
    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
        return user

    return dependency
