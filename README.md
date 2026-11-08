# TaskBoard

Учебный проект по ПМ.02 и ПМ.03: учёт задач небольшой команды.

Три роли, задачи, комментарии, статусы, Docker, PostgreSQL, CI и release build в GitHub Container Registry. Без платных сервисов.

Проект запускается на Windows, Linux и macOS.

## Стек

- Python 3.12
- FastAPI
- SQLModel
- Jinja2
- Bootstrap
- SQLite локально / PostgreSQL в Docker
- Docker Compose

## Быстрый старт

Кроссплатформенно, через Makefile:

```bash
make setup
make run
```

Открыть http://127.0.0.1:8000

Вручную без make:

Linux / macOS:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
.venv/bin/python -m uvicorn app.main:app --reload
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Демо-доступ

| Роль | Email | Пароль |
| --- | --- | --- |
| Администратор | admin@taskboard.local | admin123 |
| Руководитель | manager@taskboard.local | manager123 |
| Сотрудник | employee@taskboard.local | employee123 |

## Docker

```bash
docker compose up --build
```

## Release build

```bash
docker compose -f docker-compose.release.yml up -d
```

Готовый образ: `ghcr.io/shargabong/taskboard:v0.1.0`

## Проверки

```bash
make check
```

Линтер и тесты отдельно:

```bash
make lint
make test
```

## документация

- `docs/up02/` - учебная практика ПМ.02.
- `docs/up03/` - учебная практика ПМ.03.

## Статус

Приложение работает, Docker, тесты и линтер проверены, release build публикуется в GHCR.
