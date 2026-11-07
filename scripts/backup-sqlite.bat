@echo off
setlocal
cd /d "%~dp0.."

if not exist data\taskboard.db (
    echo Database not found: data\taskboard.db
    exit /b 1
)

if not exist backups mkdir backups

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd-HHmm"') do set stamp=%%i

copy /y data\taskboard.db backups\taskboard-sqlite-%stamp%.db >nul
if errorlevel 1 (
    echo Backup failed.
    exit /b 1
)

echo Backup created: backups\taskboard-sqlite-%stamp%.db
