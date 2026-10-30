@echo off
setlocal
cd /d "%~dp0.."

if not exist .venv\Scripts\python.exe (
    echo Virtual environment not found. Run scripts\setup.bat first.
    exit /b 1
)

.venv\Scripts\python.exe -m ruff format .
.venv\Scripts\python.exe -m ruff check --fix .
