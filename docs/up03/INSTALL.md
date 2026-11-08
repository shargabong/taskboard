# УП03. Установка и запуск

## 1. Что нужно

- Windows 10 или 11;
- Python 3.12;
- Git;
- Docker Desktop для контейнеров;
- браузер.

## 2. Локально

```powershell
cd taskboard
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Открыть http://127.0.0.1:8000

## 3. Скрипты

```powershell
scripts\setup.bat
scripts\run.bat
scripts\check.bat
scripts\format.bat
```

## 4. Docker

```powershell
docker compose up --build
```

Проверка:

```powershell
docker compose ps
```

Ожидание: `app` и `db` в статусе healthy.

## 5. Release build

```powershell
docker compose -f docker-compose.release.yml up -d
```

Если образа нет локально, он скачается из GHCR:

```text
ghcr.io/shargabong/taskboard:v0.1.0
```

## 6. Чистая установка

Проверено в отдельной папке:

```text
setup.bat -> зависимости установлены, .env создан
check.bat -> All checks passed, 16 passed in 2.10s
```

Логи: `docs/up03/clean-check-output.txt`.

## 7. Типовые проблемы

| Проблема | Решение |
| --- | --- |
| `python` не найден | Добавить Python в PATH |
| Порт 8000 занят | `--port 8001` |
| `docker` не найден | Перезапустить терминал или добавить Docker Desktop в PATH |
| База не готова | Подождать healthcheck, приложение умеет ждать базу |
| `.env` не создан | `Copy-Item .env.example .env` |

## 8. Вывод

Установка воспроизводимая. Другой человек может поднять проект по инструкции или запустить готовый образ.
