@echo off
setlocal
cd /d "%~dp0.."

echo Listening ports (8000 app, 5432 postgres):
netstat -ano | findstr ":8000"
netstat -ano | findstr ":5432"

echo Port check completed.
