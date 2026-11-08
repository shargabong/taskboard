# УП03. Сценарий демонстрации

## 1. Подготовка

```powershell
docker compose -f docker-compose.release.yml up -d
```

Проверить:

```text
http://127.0.0.1:8000/health
```

## 2. План на 5-7 минут

| Время | Что показать | Что сказать |
| --- | --- | --- |
| 0:00-0:30 | Титул и репозиторий | TaskBoard, ПМ.02 и ПМ.03 |
| 0:30-1:00 | `docker compose ps` | App и БД healthy |
| 1:00-1:30 | `/health` | 200, база доступна |
| 1:30-2:30 | Вход руководителя | Роли и главная |
| 2:30-3:30 | Задачи | Создание, фильтры, карточка |
| 3:30-4:00 | Комментарий и статус | В работе и выполнена |
| 4:00-4:30 | Сотрудник | Видит только свои задачи |
| 4:30-5:00 | Админ | Пользователи |
| 5:00-5:30 | Тесты и линтер | 16 passed, ruff clean |
| 5:30-6:00 | Release build | GHCR, тег, compose |
| 6:00-6:30 | Backup | pg_dump и restore |
| 6:30-7:00 | Итог | Что сделано и что дальше |

## 3. Демо-доступ

```text
admin@taskboard.local / admin123
manager@taskboard.local / manager123
employee@taskboard.local / employee123
```

## 4. Ключевые команды

```powershell
docker compose -f docker-compose.release.yml ps
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m pytest -v
make backup
```

## 5. Если что-то упало

1. Показать `docs/up03/screens/`.
2. Показать `docs/up03/api-test-output.txt`.
3. Показать `docs/up03/clean-check-output.txt`.
4. Показать `docs/up03/postgres-backup-restore-output.txt`.

## 6. Вывод

Проект маленький, но закрывает все этапы. Основное внимание на Docker, CI, release build, backup и безопасность.
