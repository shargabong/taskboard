from datetime import timedelta

from sqlmodel import Session, select

from app.models import Comment, Priority, Role, Task, TaskStatus, User, utc_now
from app.security import hash_password

DEFAULT_USERS = [
    ("admin@taskboard.local", "Администратор Системы", Role.admin, "admin123"),
    ("manager@taskboard.local", "Иван Петров", Role.manager, "manager123"),
    ("employee@taskboard.local", "Даниил Гущин", Role.employee, "employee123"),
    ("employee2@taskboard.local", "Ольга Смирнова", Role.employee, "employee123"),
]


def seed_demo_data(session: Session) -> None:
    if session.exec(select(User)).first():
        return

    try:
        users = {}
        for email, full_name, role, password in DEFAULT_USERS:
            user = User(
                email=email,
                full_name=full_name,
                role=role,
                password_hash=hash_password(password),
            )
            session.add(user)
            users[email] = user
        session.commit()
        for user in users.values():
            session.refresh(user)
    except Exception:
        session.rollback()
        raise

    admin = users["admin@taskboard.local"]
    manager = users["manager@taskboard.local"]
    employee = users["employee@taskboard.local"]
    employee2 = users["employee2@taskboard.local"]

    now = utc_now()
    demo_tasks = [
        {
            "title": "Подготовить отчёт за неделю",
            "description": "Собрать статусы задач и отправить руководителю.",
            "status": TaskStatus.in_progress,
            "priority": Priority.high,
            "author": manager,
            "assignee": employee,
            "created_at": now - timedelta(days=1),
        },
        {
            "title": "Обновить инструкцию по запуску",
            "description": "Проверить команды и убрать устаревшие шаги.",
            "status": TaskStatus.new,
            "priority": Priority.normal,
            "author": manager,
            "assignee": employee2,
            "created_at": now - timedelta(hours=5),
        },
        {
            "title": "Проверить резервную копию",
            "description": "Сделать backup базы и проверить восстановление.",
            "status": TaskStatus.done,
            "priority": Priority.high,
            "author": admin,
            "assignee": employee,
            "created_at": now - timedelta(days=3),
        },
        {
            "title": "Разобрать старые заявки",
            "description": "Закрыть завершённые задачи и обновить статусы.",
            "status": TaskStatus.in_progress,
            "priority": Priority.low,
            "author": admin,
            "assignee": employee2,
            "created_at": now - timedelta(days=2),
        },
        {
            "title": "Настроить уведомления в CI",
            "description": "Добавить сообщение в чат при падении сборки.",
            "status": TaskStatus.new,
            "priority": Priority.normal,
            "author": manager,
            "assignee": None,
            "created_at": now - timedelta(hours=2),
        },
    ]

    created = []
    for item in demo_tasks:
        task = Task(
            title=item["title"],
            description=item["description"],
            status=item["status"],
            priority=item["priority"],
            author_id=item["author"].id,
            assignee_id=item["assignee"].id if item["assignee"] else None,
            created_at=item["created_at"],
            updated_at=item["created_at"],
            completed_at=item["created_at"] + timedelta(hours=4)
            if item["status"] == TaskStatus.done
            else None,
        )
        session.add(task)
        created.append(task)
    session.commit()
    for task in created:
        session.refresh(task)

    session.add(Comment(task_id=created[0].id, author_id=employee.id, body="Начал собирать цифры."))
    session.add(
        Comment(
            task_id=created[0].id, author_id=manager.id, body="Не забудь про просроченные задачи."
        )
    )
    session.add(
        Comment(
            task_id=created[2].id,
            author_id=employee.id,
            body="Копия сделана, восстановление проверено.",
        )
    )
    session.commit()
