from datetime import UTC, datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class Role(StrEnum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


class TaskStatus(StrEnum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


class Priority(StrEnum):
    low = "low"
    normal = "normal"
    high = "high"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    password_hash: str
    role: Role = Field(default=Role.employee)
    is_active: bool = True
    created_at: datetime = Field(default_factory=utc_now)


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    status: TaskStatus = Field(default=TaskStatus.new)
    priority: Priority = Field(default=Priority.normal)
    author_id: int = Field(foreign_key="user.id")
    assignee_id: int | None = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True)
    author_id: int = Field(foreign_key="user.id")
    body: str
    created_at: datetime = Field(default_factory=utc_now)
