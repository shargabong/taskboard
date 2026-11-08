# Кроссплатформенный Makefile.
# Windows использует .venv/Scripts, Linux и macOS - .venv/bin.

ifeq ($(OS),Windows_NT)
    PY=.venv/Scripts/python.exe
    VENV_PY=python
else
    PY=.venv/bin/python
    VENV_PY=python3
endif

.PHONY: setup run check format test lint quality security deps backup restore backup-sqlite docker-up docker-down logs release

setup:
	$(VENV_PY) -m venv .venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements-dev.txt
	$(PY) -c "import os,shutil; shutil.copy('.env.example','.env') if not os.path.exists('.env') else None"

run:
	$(PY) -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

check: lint test

lint:
	$(PY) -m ruff check .

quality: lint test
	$(PY) -m ruff format --check .

format:
	$(PY) -m ruff format .
	$(PY) -m ruff check --fix .

test:
	$(PY) -m pytest

security:
	$(PY) scripts/security_check.py

deps:
	$(PY) -m pip install pip-audit >/dev/null 2>&1 || true
	$(PY) -m pip_audit -r requirements.txt

backup:
	$(PY) scripts/backup.py

backup-sqlite:
	$(PY) scripts/backup.py --sqlite

restore:
	$(PY) scripts/restore.py $(FILE)

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f app

release:
	docker build -t ghcr.io/shargabong/taskboard:v0.1.0 .
	docker compose -f docker-compose.release.yml up -d
