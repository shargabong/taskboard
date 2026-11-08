# Этап 12. Портфолио

## 12.1. Состав

| Материал | Путь |
| --- | --- |
| Код | `app/` |
| Тесты | `tests/` |
| Docker | `Dockerfile`, `docker-compose.yml`, `docker-compose.release.yml` |
| CI | `.github/workflows/ci.yml` |
| Release | `.github/workflows/release.yml` |
| Скрипты | `scripts/` |
| Документы УП02 | `docs/up02/` |
| Документы УП03 | `docs/up03/` |
| Отчёт УП02 | `docs/up02/otchet_UP02_Gushchin.docx` |
| Отчёт УП03 | `docs/up03/otchet_UP03_Gushchin.docx` |

## 12.2. Как проверить

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Docker:

```powershell
docker compose up --build
```

Release build:

```powershell
docker compose -f docker-compose.release.yml up -d
```

## 12.3. Компетенции

| Компетенция | Подтверждение |
| --- | --- |
| ПК 2.1 | ТЗ и требования |
| ПК 2.2 | Рабочее приложение и Docker |
| ПК 2.3 | Отладка и журнал ошибок |
| ПК 2.4 | 16 тестов |
| ПК 2.5 | ruff и инспекция |

## 12.4. Вывод

Проект небольшой, но закрывает все этапы практики. Основной сценарий работает, тесты проходят, инфраструктура проверена. Материалы позволяют проверить результат без устных пояснений.
