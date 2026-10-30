from tests.conftest import login


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "Вход в TaskBoard" in response.text


def test_dashboard_requires_login(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")


def test_manager_login_and_dashboard(client):
    response = login(client, "manager@taskboard.local", "manager123")
    assert response.status_code == 303
    page = client.get("/")
    assert page.status_code == 200
    assert "Сводка" in page.text


def test_employee_sees_only_own_tasks(client):
    login(client, "employee@taskboard.local", "employee123")
    response = client.get("/tasks")
    assert response.status_code == 200
    assert "Подготовить отчёт за неделю" in response.text
    assert "Обновить инструкцию по запуску" not in response.text


def test_create_task_as_manager(client):
    login(client, "manager@taskboard.local", "manager123")
    response = client.post(
        "/tasks/new",
        data={
            "title": "Тестовая задача из pytest",
            "description": "Проверка создания задачи.",
            "priority": "high",
            "assignee_id": "",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    location = response.headers["location"]
    assert location.startswith("/tasks/")
    page = client.get(location)
    assert page.status_code == 200
    assert "Тестовая задача из pytest" in page.text


def test_comment_on_own_task(client):
    login(client, "employee@taskboard.local", "employee123")
    response = client.post(
        "/tasks/1/comment",
        data={"body": "Комментарий из автотеста"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Комментарий из автотеста" in response.text


def test_employee_cannot_view_foreign_task(client):
    login(client, "employee@taskboard.local", "employee123")
    response = client.get("/tasks/2")
    assert response.status_code == 403


def test_manager_can_change_status(client):
    login(client, "manager@taskboard.local", "manager123")
    created = client.post(
        "/tasks/new",
        data={
            "title": "Задача для смены статуса",
            "description": "Проверяем переходы.",
            "priority": "normal",
            "assignee_id": "",
        },
        follow_redirects=False,
    )
    task_url = created.headers["location"]
    in_progress = client.post(
        f"{task_url}/status",
        data={"new_status": "in_progress"},
        follow_redirects=True,
    )
    assert in_progress.status_code == 200
    done = client.post(
        f"{task_url}/status",
        data={"new_status": "done"},
        follow_redirects=True,
    )
    assert done.status_code == 200
    assert "Выполнена" in done.text


def test_admin_creates_user(client):
    login(client, "admin@taskboard.local", "admin123")
    response = client.post(
        "/admin/users",
        data={
            "full_name": "Новый Сотрудник",
            "email": "new.user@taskboard.local",
            "role": "employee",
            "password": "password123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "new.user@taskboard.local" in response.text


def test_employee_cannot_access_admin(client):
    login(client, "employee@taskboard.local", "employee123")
    response = client.get("/admin/users")
    assert response.status_code == 403
