# Release Notes

## TaskBoard 0.1.0

Дата: 2026-11-04

### Что это

Учебная система учёта задач небольшой команды. Три роли, задачи, комментарии, статусы, Docker, PostgreSQL и release build.

### Образ

```text
ghcr.io/shargabong/taskboard:v0.1.0
```

### Запуск

```powershell
docker compose -f docker-compose.release.yml up -d
```

Проверка:

```text
GET http://127.0.0.1:8000/health
```

### Проверки

```text
ruff check . -> All checks passed
pytest -> 15 passed
POST /login -> 200
GET /tasks -> 200
Backup/restore PostgreSQL -> OK
pip-audit -> No known vulnerabilities found
```

### Известные ограничения

- нет CSRF;
- нет rate limit;
- нет миграций;
- демо-пароли;
- нет внешнего мониторинга.

### Ссылки

- `docs/up02/` - ПМ.02.
- `docs/up03/` - ПМ.03.
- `docs/up03/DEMO_SCRIPT.md` - демонстрация.
