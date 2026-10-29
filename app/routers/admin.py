from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import require_roles
from app.models import Role, User
from app.security import hash_password
from app.web import flash, render

router = APIRouter(prefix="/admin")


@router.get("/users")
def users_page(
    request: Request,
    user: User = Depends(require_roles(Role.admin)),
    session: Session = Depends(get_session),
):
    users = list(session.exec(select(User).order_by(User.full_name)).all())
    return render(
        request,
        "admin/users.html",
        {"user": user, "users": users, "roles": list(Role)},
    )


@router.post("/users")
def user_create(
    request: Request,
    email: str = Form(...),
    full_name: str = Form(...),
    role: str = Form("employee"),
    password: str = Form(...),
    user: User = Depends(require_roles(Role.admin)),
    session: Session = Depends(get_session),
):
    normalized = email.strip().lower()
    if not normalized or not full_name.strip():
        flash(request, "Заполните email и имя", "danger")
        return RedirectResponse("/admin/users", status_code=303)
    if len(password) < 6:
        flash(request, "Пароль должен быть не короче 6 символов", "danger")
        return RedirectResponse("/admin/users", status_code=303)
    existing = session.exec(select(User).where(User.email == normalized)).first()
    if existing is not None:
        flash(request, "Пользователь с таким email уже существует", "danger")
        return RedirectResponse("/admin/users", status_code=303)
    try:
        selected_role = Role(role)
    except ValueError:
        selected_role = Role.employee
    new_user = User(
        email=normalized,
        full_name=full_name.strip(),
        role=selected_role,
        password_hash=hash_password(password),
    )
    session.add(new_user)
    session.commit()
    flash(request, f"Пользователь {new_user.full_name} создан")
    return RedirectResponse("/admin/users", status_code=303)


@router.post("/users/{user_id}/toggle")
def user_toggle(
    user_id: int,
    request: Request,
    user: User = Depends(require_roles(Role.admin)),
    session: Session = Depends(get_session),
):
    target = session.get(User, user_id)
    if target is None:
        flash(request, "Пользователь не найден", "danger")
        return RedirectResponse("/admin/users", status_code=303)
    if target.id == user.id:
        flash(request, "Нельзя отключить самого себя", "danger")
        return RedirectResponse("/admin/users", status_code=303)
    target.is_active = not target.is_active
    session.add(target)
    session.commit()
    flash(request, "Статус пользователя изменён")
    return RedirectResponse("/admin/users", status_code=303)
