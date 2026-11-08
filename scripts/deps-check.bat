@echo off
setlocal
cd /d "%~dp0.."

if not exist .venv\Scripts\python.exe (
    echo Virtual environment not found. Run scripts\setup.bat first.
    exit /b 1
)

echo Checking dependencies for known vulnerabilities...
.venv\Scripts\python.exe -m pip install pip-audit >nul 2>&1
.venv\Scripts\python.exe -m pip_audit -r requirements.txt
echo Dependency check completed.
