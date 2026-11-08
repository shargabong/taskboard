"""Проверки безопасности TaskBoard (кроссплатформенно).

Запуск: python scripts/security_check.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def tracked_secrets() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, cwd=ROOT,
    )
    bad = []
    for name in result.stdout.splitlines():
        low = name.lower()
        if low.endswith((".env", ".pem", ".key")) and ".example" not in low:
            bad.append(name)
    return bad


def main() -> int:
    print("== Проверка безопасности ==\n")

    secrets = tracked_secrets()
    print("Секреты в репозитории:")
    print("  " + ("нет" if not secrets else ", ".join(secrets)))

    print("\nРежим отладки по умолчанию:")
    config = (ROOT / "app" / "config.py").read_text(encoding="utf-8")
    for line in config.splitlines():
        if "debug" in line.lower():
            print("  " + line.strip())

    print("\nХеширование паролей:")
    security = (ROOT / "app" / "security.py").read_text(encoding="utf-8")
    print("  PBKDF2: " + ("да" if "pbkdf2" in security.lower() else "не найдено"))

    ok = not secrets
    print("\nИтог:", "ок" if ok else "есть замечания")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
