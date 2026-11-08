@echo off
setlocal
cd /d "%~dp0.."

if not exist .venv\Scripts\python.exe (
    echo Virtual environment not found. Run scripts\setup.bat first.
    exit /b 1
)

echo Running linter...
.venv\Scripts\python.exe -m ruff check .
if errorlevel 1 exit /b 1

echo Formatting check...
.venv\Scripts\python.exe -m ruff format --check .
if errorlevel 1 exit /b 1

echo Running tests...
.venv\Scripts\python.exe -m pytest

echo Quality check completed.
