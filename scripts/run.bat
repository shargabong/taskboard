@echo off
setlocal
cd /d "%~dp0.."

if not exist .venv\Scripts\python.exe (
    echo Virtual environment not found. Run scripts\setup.bat first.
    exit /b 1
)

if not exist .env (
    copy .env.example .env >nul
)

.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
