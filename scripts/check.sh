#!/usr/bin/env bash
# Линтер и тесты
set -e
cd "$(dirname "$0")/.."

if [ ! -x .venv/bin/python ]; then
    echo "Virtual environment not found. Run scripts/setup.sh first."
    exit 1
fi

echo "Running linter..."
.venv/bin/python -m ruff check .

echo "Running tests..."
.venv/bin/python -m pytest
