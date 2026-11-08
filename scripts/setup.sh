#!/usr/bin/env bash
# Создаёт окружение, ставит зависимости и готовит .env
set -e
cd "$(dirname "$0")/.."

PY=${PYTHON:-python3}

$PY -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt

if [ ! -f .env ]; then
    cp .env.example .env
fi

echo "Setup completed. Run scripts/run.sh to start the app."
