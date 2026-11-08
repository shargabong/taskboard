#!/usr/bin/env bash
# Запускает приложение
set -e
cd "$(dirname "$0")/.."

if [ ! -x .venv/bin/python ]; then
    echo "Virtual environment not found. Run scripts/setup.sh first."
    exit 1
fi

.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
