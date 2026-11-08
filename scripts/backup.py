"""Резервное копирование базы TaskBoard (кроссплатформенно).

Использование:
    python scripts/backup.py           # бэкап: PostgreSQL через docker, иначе SQLite
    python scripts/backup.py --sqlite  # только SQLite-файл
"""
import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUPS = ROOT / "backups"
STAMP = datetime.now().strftime("%Y-%m-%d-%H%M")


def backup_postgres() -> int:
    BACKUPS.mkdir(exist_ok=True)
    out = BACKUPS / f"taskboard-{STAMP}.sql"
    try:
        with out.open("wb") as f:
            result = subprocess.run(
                ["docker", "compose", "exec", "-T", "db",
                 "pg_dump", "-U", "taskboard", "taskboard"],
                stdout=f, stderr=subprocess.PIPE, cwd=ROOT,
            )
    except FileNotFoundError:
        print("docker не найден. Для PostgreSQL-бэкапа нужен Docker.")
        return 1
    if result.returncode != 0:
        out.unlink(missing_ok=True)
        print("Бэкап не удался. Запущен ли контейнер db?")
        print(result.stderr.decode("utf-8", "replace"))
        return 1
    print(f"Бэкап создан: {out.relative_to(ROOT)}")
    return 0


def backup_sqlite() -> int:
    src = ROOT / "data" / "taskboard.db"
    if not src.exists():
        print(f"База не найдена: {src.relative_to(ROOT)}")
        return 1
    BACKUPS.mkdir(exist_ok=True)
    dst = BACKUPS / f"taskboard-sqlite-{STAMP}.db"
    shutil.copy2(src, dst)
    print(f"Бэкап создан: {dst.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sqlite", action="store_true", help="только SQLite")
    args = parser.parse_args()
    if args.sqlite:
        return backup_sqlite()
    if (ROOT / "data" / "taskboard.db").exists():
        return backup_sqlite()
    return backup_postgres()


if __name__ == "__main__":
    sys.exit(main())
