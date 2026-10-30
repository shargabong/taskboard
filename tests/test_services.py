from app.models import Priority, Role, Task, TaskStatus, User
from app.security import hash_password, verify_password
from app.services.tasks import can_change_status


def test_password_hash_and_verify():
    stored = hash_password("secret123")
    assert stored != "secret123"
    assert verify_password("secret123", stored)
    assert not verify_password("wrong", stored)
    assert not verify_password("secret123", "broken")


def test_status_transitions_for_employee():
    employee = User(
        id=3,
        email="employee@test.local",
        full_name="Employee",
        password_hash="x",
        role=Role.employee,
    )
    own_task = Task(
        id=1,
        title="Task",
        description="Description",
        author_id=2,
        assignee_id=3,
        status=TaskStatus.new,
    )
    foreign_task = Task(
        id=2,
        title="Task",
        description="Description",
        author_id=2,
        assignee_id=4,
        status=TaskStatus.new,
    )
    assert can_change_status(employee, own_task, TaskStatus.in_progress)
    assert not can_change_status(employee, foreign_task, TaskStatus.in_progress)


def test_status_transitions_for_manager():
    manager = User(
        id=2,
        email="manager@test.local",
        full_name="Manager",
        password_hash="x",
        role=Role.manager,
    )
    task = Task(
        id=1,
        title="Task",
        description="Description",
        author_id=2,
        assignee_id=3,
        status=TaskStatus.new,
    )
    assert can_change_status(manager, task, TaskStatus.in_progress)
    assert can_change_status(manager, task, TaskStatus.done)
    task.status = TaskStatus.done
    assert can_change_status(manager, task, TaskStatus.in_progress)
    assert not can_change_status(manager, task, TaskStatus.done)


def test_priority_values():
    assert Priority.low.value == "low"
    assert Priority.high.value == "high"
