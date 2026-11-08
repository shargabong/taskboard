# УП03. Конфигурация

## 1. Переменные

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `TASKBOARD_ENVIRONMENT` | development | Среда |
| `TASKBOARD_DEBUG` | false | SQL-логи |
| `TASKBOARD_SECRET_KEY` | dev-secret-change-me | Подпись cookie |
| `TASKBOARD_DATABASE_URL` | sqlite:///./data/taskboard.db | База |
| `TASKBOARD_SESSION_COOKIE` | taskboard_session | Имя cookie |
| `TASKBOARD_SESSION_HTTPS_ONLY` | false | Cookie только по HTTPS |
| `TASKBOARD_SEED_DEMO` | true | Демо-данные |

## 2. Development

```env
TASKBOARD_ENVIRONMENT=development
TASKBOARD_DEBUG=false
TASKBOARD_SECRET_KEY=change-me
TASKBOARD_DATABASE_URL=sqlite:///./data/taskboard.db
TASKBOARD_SESSION_HTTPS_ONLY=false
TASKBOARD_SEED_DEMO=true
```

## 3. Production

```env
TASKBOARD_ENVIRONMENT=production
TASKBOARD_DEBUG=false
TASKBOARD_SECRET_KEY=<случайная строка>
TASKBOARD_DATABASE_URL=postgresql://taskboard:password@db:5432/taskboard
TASKBOARD_SESSION_HTTPS_ONLY=true
TASKBOARD_SEED_DEMO=true
```

## 4. Строки подключения

| База | Строка |
| --- | --- |
| SQLite | `sqlite:///./data/taskboard.db` |
| PostgreSQL локально | `postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard` |
| PostgreSQL в Docker | `postgresql+psycopg://taskboard:taskboard@db:5432/taskboard` |

## 5. Секреты

- `.env` и `.env.production` в `.gitignore`.
- В репозитории только примеры.
- Пароли в базе в виде PBKDF2.
- Демо-пароли только для учебного запуска.

## 6. Проверка

```text
GET /health -> {"status":"ok","environment":"production"}
```

## 7. Вывод

Конфигурация простая: одна строка базы и несколько флагов. Этого достаточно для локального запуска, Docker и release build.
