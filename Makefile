PY=.venv/Scripts/python.exe

.PHONY: setup run check format test lint docker-up docker-down logs release

setup:
	python -m venv .venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements-dev.txt
	if not exist .env copy .env.example .env

run:
	$(PY) -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

check: lint test

lint:
	$(PY) -m ruff check .

format:
	$(PY) -m ruff format .
	$(PY) -m ruff check --fix .

test:
	$(PY) -m pytest

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f app

release:
	docker build -t ghcr.io/shargabong/taskboard:v0.1.0 .
	docker compose -f docker-compose.release.yml up -d
