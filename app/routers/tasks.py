from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.db import get_session
from app.dependencies import get_current_user
from app.models import Priority, Role, Task, TaskStatus, User
from app.services.tasks import (
    add_comment,
    can_change_status,
    can_view,
    change_status,
    create_task,
    dashboard_stats,
    list_assignees,
    list_tasks,
    task_detail,
    tasks_view,
)
from app.web import flash, render

router = APIRouter()


def parse_status(value: str | None) -> TaskStatus | None:
    if not value:
        return None
    try:
        return TaskStatus(value)
    except ValueError:
        return None


def parse_priority(value: str | None) -> Priority | None:
    if not value:
        return None
    try:
        return Priority(value)
    except ValueError:
        return None


def get_task_for_user(session: Session, task_id: int, user: User) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    if not can_view(user, task):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к задаче")
    return task


@router.get("/")
def dashboard(
    request: Request,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stats = dashboard_stats(session, user)
    return render(
        request,
        "dashboard.html",
        {
            "user": user,
            "stats": stats,
            "recent": tasks_view(session, stats["recent"]),
        },
    )


@router.get("/tasks")
def tasks_list(
    request: Request,
    status: str | None = None,
    assignee_id: int | None = None,
    mine: bool = False,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    selected_status = parse_status(status)
    tasks = list_tasks(
        session,
        user,
        status=selected_status,
        assignee_id=assignee_id,
        mine=mine,
    )
    return render(
        request,
        "tasks/list.html",
        {
            "user": user,
            "tasks": tasks_view(session, tasks),
            "selected_status": selected_status,
            "selected_assignee": assignee_id,
            "mine": mine,
            "assignees": list_assignees(session, user),
        },
    )


@router.get("/tasks/new")
def task_form(
    request: Request,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return render(
        request,
        "tasks/form.html",
        {"user": user, "assignees": list_assignees(session, user)},
    )


@router.post("/tasks/new")
def task_create(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form("normal"),
    assignee_id: int | None = Form(None),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not title.strip() or not description.strip():
        flash(request, "Заполните название и описание", "danger")
        return RedirectResponse("/tasks/new", status_code=303)
    selected_priority = parse_priority(priority) or Priority.normal
    if user.role == Role.employee:
        assignee_id = user.id
    try:
        task = create_task(
            session,
            user,
            title,
            description,
            selected_priority,
            assignee_id,
        )
    except ValueError:
        flash(request, "Исполнитель недоступен", "danger")
        return RedirectResponse("/tasks/new", status_code=303)
    flash(request, f"Задача #{task.id} создана")
    return RedirectResponse(f"/tasks/{task.id}", status_code=303)


@router.get("/tasks/{task_id}")
def task_page(
    task_id: int,
    request: Request,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = get_task_for_user(session, task_id, user)
    detail = task_detail(session, task)
    allowed_statuses = [item for item in TaskStatus if can_change_status(user, task, item)]
    return render(
        request,
        "tasks/detail.html",
        {
            "user": user,
            **detail,
            "allowed_statuses": allowed_statuses,
            "can_assign": user.role in (Role.admin, Role.manager),
            "assignees": list_assignees(session, user),
        },
    )


@router.post("/tasks/{task_id}/comment")
def task_comment(
    task_id: int,
    request: Request,
    body: str = Form(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = get_task_for_user(session, task_id, user)
    if not body.strip():
        flash(request, "Комментарий не может быть пустым", "danger")
        return RedirectResponse(f"/tasks/{task.id}", status_code=303)
    add_comment(session, task, user, body)
    flash(request, "Комментарий добавлен")
    return RedirectResponse(f"/tasks/{task.id}", status_code=303)


@router.post("/tasks/{task_id}/status")
def task_status(
    task_id: int,
    request: Request,
    new_status: str = Form(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = get_task_for_user(session, task_id, user)
    selected = parse_status(new_status)
    if selected is None or not can_change_status(user, task, selected):
        flash(request, "Этот переход статуса недоступен", "danger")
        return RedirectResponse(f"/tasks/{task.id}", status_code=303)
    try:
        change_status(session, task, selected)
    except ValueError:
        flash(request, "Недопустимый переход статуса", "danger")
        return RedirectResponse(f"/tasks/{task.id}", status_code=303)
    flash(request, "Статус обновлён")
    return RedirectResponse(f"/tasks/{task.id}", status_code=303)


@router.post("/tasks/{task_id}/assign")
def task_assign(
    task_id: int,
    request: Request,
    assignee_id: int = Form(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if user.role not in (Role.admin, Role.manager):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    task = get_task_for_user(session, task_id, user)
    assignee = session.get(User, assignee_id)
    if assignee is None or not assignee.is_active:
        flash(request, "Исполнитель недоступен", "danger")
        return RedirectResponse(f"/tasks/{task.id}", status_code=303)
    task.assignee_id = assignee.id
    session.add(task)
    session.commit()
    flash(request, f"Исполнитель: {assignee.full_name}")
    return RedirectResponse(f"/tasks/{task.id}", status_code=303)
