from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import get_optional_user
from app.models import User
from app.security import verify_password
from app.web import flash, render

router = APIRouter()


def safe_next(value: str | None) -> str:
    if not value or not value.startswith("/") or value.startswith("//"):
        return "/"
    return value


@router.get("/login")
def login_form(
    request: Request,
    next: str = "/",
    user: User | None = Depends(get_optional_user),
):
    if user is not None:
        return RedirectResponse("/", status_code=303)
    return render(request, "login.html", {"next": safe_next(next)})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    next: str = Form("/"),
    session: Session = Depends(get_session),
):
    normalized = email.strip().lower()
    user = session.exec(select(User).where(User.email == normalized)).first()
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        return render(
            request,
            "login.html",
            {"error": "Неверный email или пароль", "next": safe_next(next)},
            status_code=400,
        )
    request.session.clear()
    request.session["user_id"] = user.id
    flash(request, f"Добро пожаловать, {user.full_name}")
    return RedirectResponse(safe_next(next), status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)
