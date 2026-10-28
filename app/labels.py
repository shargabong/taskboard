from app.models import Priority, Role, TaskStatus

ROLE_LABELS = {
    Role.admin: "Администратор",
    Role.manager: "Руководитель",
    Role.employee: "Сотрудник",
}

STATUS_LABELS = {
    TaskStatus.new: "Новая",
    TaskStatus.in_progress: "В работе",
    TaskStatus.done: "Выполнена",
}

PRIORITY_LABELS = {
    Priority.low: "Низкий",
    Priority.normal: "Обычный",
    Priority.high: "Высокий",
}

STATUS_CLASSES = {
    TaskStatus.new: "secondary",
    TaskStatus.in_progress: "primary",
    TaskStatus.done: "success",
}

PRIORITY_CLASSES = {
    Priority.low: "light",
    Priority.normal: "info",
    Priority.high: "warning",
}


def format_dt(value) -> str:
    if value is None:
        return "не задано"
    return value.strftime("%d.%m.%Y %H:%M")
