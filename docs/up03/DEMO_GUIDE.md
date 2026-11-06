# УП03. Руководство по демонстрации

## 1. Запуск

```powershell
docker compose -f docker-compose.release.yml up -d
```

Проверка:

```text
http://127.0.0.1:8000/health
```

## 2. Что показать

1. `docker compose -f docker-compose.release.yml ps`: app и db healthy.
2. `/health`: 200, production.
3. Вход руководителем: `manager@taskboard.local / manager123`.
4. Главная: счётчики задач.
5. Список задач и фильтры.
6. Карточка задачи, комментарий.
7. Смена статуса на «В работе» и «Выполнена».
8. Вход сотрудником: видны только свои задачи.
9. Вход администратором: управление пользователями.
10. Тесты и линтер: `15 passed`, `ruff` чистый.
11. Release build: образ `ghcr.io/shargabong/taskboard:v0.1.0`.
12. Backup и restore PostgreSQL.

## 3. Демо-доступ

```text
admin@taskboard.local / admin123
manager@taskboard.local / manager123
employee@taskboard.local / employee123
```

## 4. Если что-то не запускается

- проверить `docker compose ps`;
- проверить логи `docker compose logs app`;
- проверить `/health`;
- поднять заново `docker compose -f docker-compose.release.yml up -d`.

## 5. Вывод

Демонстрация занимает 5-7 минут. Основной акцент на роли, задачи, Docker, CI, release build и backup.
