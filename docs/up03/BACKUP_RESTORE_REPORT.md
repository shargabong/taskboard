# УП03. Резервное копирование и восстановление

## 1. Что проверялось

- дамп PostgreSQL;
- восстановление в отдельную базу;
- сравнение количества задач;
- удаление тестовой базы.

## 2. Схема

![Backup flow](diagrams/backup-flow.png)

## 3. Команды

```powershell
docker compose exec -T db createdb -U taskboard taskboard_restore
docker compose exec -T db pg_dump -U taskboard taskboard > backups\taskboard-postgres.sql
docker compose exec -T db psql -U taskboard -d taskboard_restore < backups\taskboard-postgres.sql
docker compose exec -T db psql -U taskboard -d taskboard -tAc "select count(*) from task;"
docker compose exec -T db psql -U taskboard -d taskboard_restore -tAc "select count(*) from task;"
docker compose exec -T db dropdb -U taskboard --if-exists taskboard_restore
```

## 4. Фактический результат

```text
dump size: 9506 bytes
source task count: 6
restored task count: 6
RESULT: OK
```

Полный вывод: `docs/up03/postgres-backup-restore-output.txt`.

## 5. Скрипты

- `scripts/backup-db.bat`;
- `scripts/restore-db.bat`;
- `scripts/backup-sqlite.bat`.

## 6. Стратегия

| Параметр | Значение |
| --- | --- |
| Что копируется | PostgreSQL |
| Частота | Перед релизом и раз в сутки для демо |
| Хранение | 3 последние копии |
| RPO | до 24 часов |
| RTO | до 1 часа |

## 7. Вывод

Backup и restore PostgreSQL проверены. Данные восстанавливаются, количество задач совпадает.
