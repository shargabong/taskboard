@echo off
setlocal
cd /d "%~dp0.."

echo Building release image...
docker build -t ghcr.io/shargabong/taskboard:v0.1.0 .
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo Build completed: ghcr.io/shargabong/taskboard:v0.1.0
