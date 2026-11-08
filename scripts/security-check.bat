@echo off
setlocal
cd /d "%~dp0.."

echo == Security checklist ==
echo Secrets in repository (should be none):
git ls-files | findstr /i ".env .pem .key" | findstr /v ".env.example" | findstr /v ".env.production.example"
echo.

echo Demo passwords in code (expected for training build):
findstr /s /i "admin123 manager123 employee123" app\*.py

echo.
echo Debug mode default:
findstr /s /i "debug" app\config.py

echo.
echo Security check completed.
