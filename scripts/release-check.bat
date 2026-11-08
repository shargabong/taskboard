@echo off
setlocal
cd /d "%~dp0.."

echo == Release check ==

echo 1. Lint and tests...
call scripts\check.bat
if errorlevel 1 exit /b 1

echo 2. Image present...
docker image inspect ghcr.io/shargabong/taskboard:v0.1.0 >nul 2>&1
if errorlevel 1 (
    echo Image not found. Run scripts\build.bat first.
    exit /b 1
)

echo 3. Release compose config...
docker compose -f docker-compose.release.yml config >nul
if errorlevel 1 (
    echo Release compose config invalid.
    exit /b 1
)

echo Release check completed.
