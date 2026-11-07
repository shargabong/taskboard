@echo off
setlocal
cd /d "%~dp0.."

set "DOCKER=docker"
where docker >nul 2>&1
if errorlevel 1 set "DOCKER=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin\docker.exe"

if "%~1"=="" (
    echo Usage: scripts\restore-db.bat backups\taskboard-YYYY-MM-DD-HHmm.sql
    exit /b 1
)

if not exist "%~1" (
    echo File not found: %~1
    exit /b 1
)

"%DOCKER%" compose exec -T db psql -U taskboard -d taskboard < "%~1"
if errorlevel 1 (
    echo Restore failed.
    exit /b 1
)

echo Restore completed from %~1
