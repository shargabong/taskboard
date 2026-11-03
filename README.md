# TaskBoard

Учебный проект по ПМ.02 и ПМ.03: учёт задач небольшой команды.

Три роли, задачи, комментарии, статусы, Docker, PostgreSQL, CI и release build в GitHub Container Registry. Без платных сервисов.

## Стек

- Python 3.12
- FastAPI
- SQLModel
- Jinja2
- Bootstrap
- SQLite локально / PostgreSQL в Docker
- Docker Compose

## Быстрый старт

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Открыть http://127.0.0.1:8000

## Демо-доступ

| Роль | Email | Пароль |
| --- | --- | --- |
| Администратор | admin@taskboard.local | admin123 |
| Руководитель | manager@taskboard.local | manager123 |
| Сотрудник | employee@taskboard.local | employee123 |

## Docker

```powershell
docker compose up --build
```

## Release build

```powershell
docker compose -f docker-compose.release.yml up -d
```

Готовый образ: `ghcr.io/shargabong/taskboard:v0.1.0`

## Проверки

```powershell
scripts\check.bat
```

Или:

```powershell
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m pytest -v
```

## Документация

- `docs/up02/` - учебная практика ПМ.02.
- `docs/up03/` - учебная практика ПМ.03.

## Статус

Локально приложение работает. Docker, тесты и линтер проверены. Дальше release build в GHCR и короткие документы по практике.
