from sqlmodel import Session, select

from app.models import Comment, Priority, Role, Task, TaskStatus, User, utc_now

ALLOWED_TRANSITIONS = {
    TaskStatus.new: {TaskStatus.in_progress, TaskStatus.done},
    TaskStatus.in_progress: {TaskStatus.done, TaskStatus.new},
    TaskStatus.done: {TaskStatus.in_progress},
}


def can_view(user: User, task: Task) -> bool:
    if user.role in (Role.admin, Role.manager):
        return True
    return task.author_id == user.id or task.assignee_id == user.id


def can_change_status(user: User, task: Task, new_status: TaskStatus) -> bool:
    if new_status not in ALLOWED_TRANSITIONS.get(task.status, set()):
        return False
    if user.role in (Role.admin, Role.manager):
        return True
    return task.assignee_id == user.id


def create_task(
    session: Session,
    author: User,
    title: str,
    description: str,
    priority: Priority,
    assignee_id: int | None,
) -> Task:
    if author.role == Role.employee:
        assignee_id = author.id
    elif assignee_id is not None:
        assignee = session.get(User, assignee_id)
        if assignee is None or not assignee.is_active:
            raise ValueError("Исполнитель недоступен")
    task = Task(
        title=title.strip(),
        description=description.strip(),
        priority=priority,
        author_id=author.id,
        assignee_id=assignee_id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def add_comment(session: Session, task: Task, author: User, body: str) -> Comment:
    comment = Comment(task_id=task.id, author_id=author.id, body=body.strip())
    session.add(comment)
    task.updated_at = utc_now()
    session.add(task)
    session.commit()
    session.refresh(comment)
    return comment


def change_status(session: Session, task: Task, new_status: TaskStatus) -> Task:
    if new_status not in ALLOWED_TRANSITIONS.get(task.status, set()):
        raise ValueError("Недопустимый переход статуса")
    task.status = new_status
    task.updated_at = utc_now()
    task.completed_at = utc_now() if new_status == TaskStatus.done else None
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def list_tasks(
    session: Session,
    user: User,
    status: TaskStatus | None = None,
    assignee_id: int | None = None,
    mine: bool = False,
) -> list[Task]:
    statement = select(Task)
    if user.role == Role.employee:
        statement = statement.where((Task.author_id == user.id) | (Task.assignee_id == user.id))
    elif mine:
        statement = statement.where(Task.assignee_id == user.id)
    if status is not None:
        statement = statement.where(Task.status == status)
    if assignee_id is not None:
        statement = statement.where(Task.assignee_id == assignee_id)
    statement = statement.order_by(Task.created_at.desc())
    return list(session.exec(statement).all())


def tasks_view(session: Session, tasks: list[Task]) -> list[dict]:
    user_ids = set()
    for task in tasks:
        user_ids.add(task.author_id)
        if task.assignee_id:
            user_ids.add(task.assignee_id)
    users = {}
    if user_ids:
        users = {u.id: u for u in session.exec(select(User).where(User.id.in_(user_ids))).all()}
    return [
        {
            "task": task,
            "author": users.get(task.author_id),
            "assignee": users.get(task.assignee_id),
        }
        for task in tasks
    ]


def task_detail(session: Session, task: Task) -> dict:
    author = session.get(User, task.author_id)
    assignee = session.get(User, task.assignee_id) if task.assignee_id else None
    comments = list(
        session.exec(
            select(Comment).where(Comment.task_id == task.id).order_by(Comment.created_at.asc())
        ).all()
    )
    comment_authors = {}
    if comments:
        ids = {comment.author_id for comment in comments}
        comment_authors = {
            user.id: user for user in session.exec(select(User).where(User.id.in_(ids))).all()
        }
    return {
        "task": task,
        "author": author,
        "assignee": assignee,
        "comments": [
            {"comment": comment, "author": comment_authors.get(comment.author_id)}
            for comment in comments
        ],
    }


def dashboard_stats(session: Session, user: User) -> dict:
    tasks = list_tasks(session, user)
    counts = {status: 0 for status in TaskStatus}
    for task in tasks:
        counts[task.status] += 1
    return {
        "total": len(tasks),
        "counts": counts,
        "recent": tasks[:5],
    }


def list_assignees(session: Session, user: User) -> list[User]:
    if user.role == Role.employee:
        return [user]
    return list(
        session.exec(
            select(User).where(User.is_active == True).order_by(User.full_name)  # noqa: E712
        ).all()
    )
