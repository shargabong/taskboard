@echo off
setlocal
cd /d "%~dp0.."

set "DOCKER=docker"
where docker >nul 2>&1
if errorlevel 1 set "DOCKER=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin\docker.exe"

if not exist backups mkdir backups

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd-HHmm"') do set stamp=%%i

"%DOCKER%" compose exec -T db pg_dump -U taskboard taskboard > backups\taskboard-%stamp%.sql
if errorlevel 1 (
    echo Backup failed. Is the db container running?
    exit /b 1
)

echo Backup created: backups\taskboard-%stamp%.sql
