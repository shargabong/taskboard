from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.labels import (
    PRIORITY_CLASSES,
    PRIORITY_LABELS,
    ROLE_LABELS,
    STATUS_CLASSES,
    STATUS_LABELS,
    format_dt,
)
from app.models import Priority, Role, TaskStatus

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
templates.env.globals.update(
    role_labels=ROLE_LABELS,
    status_labels=STATUS_LABELS,
    priority_labels=PRIORITY_LABELS,
    status_classes=STATUS_CLASSES,
    priority_classes=PRIORITY_CLASSES,
    format_dt=format_dt,
    Role=Role,
    TaskStatus=TaskStatus,
    Priority=Priority,
)


def flash(request: Request, message: str, kind: str = "success") -> None:
    request.session["flash"] = {"message": message, "kind": kind}


def render(
    request: Request,
    name: str,
    context: dict[str, Any] | None = None,
    status_code: int = 200,
):
    data = {"request": request, "user": None, "flash": request.session.pop("flash", None)}
    if context:
        data.update(context)
    return templates.TemplateResponse(request, name, data, status_code=status_code)
