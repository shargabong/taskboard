"""Восстановление базы TaskBoard (кроссплатформенно).

Использование:
    python scripts/restore.py backups/taskboard-YYYY-MM-DD-HHmm.sql
    python scripts/restore.py backups/taskboard-sqlite-YYYY-MM-DD-HHmm.db
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def restore_postgres(path: Path) -> int:
    try:
        with path.open("rb") as f:
            result = subprocess.run(
                ["docker", "compose", "exec", "-T", "db",
                 "psql", "-U", "taskboard", "-d", "taskboard"],
                stdin=f, cwd=ROOT,
            )
    except FileNotFoundError:
        print("docker не найден. Для восстановления PostgreSQL нужен Docker.")
        return 1
    if result.returncode != 0:
        print("Восстановление не удалось.")
        return 1
    print(f"Восстановлено из {path}")
    return 0


def restore_sqlite(path: Path) -> int:
    dst = ROOT / "data" / "taskboard.db"
    dst.parent.mkdir(exist_ok=True)
    shutil.copy2(path, dst)
    print(f"Восстановлено из {path}")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Использование: python scripts/restore.py <файл-бэкапа>")
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Файл не найден: {path}")
        return 1
    if path.suffix == ".db":
        return restore_sqlite(path)
    return restore_postgres(path)


if __name__ == "__main__":
    sys.exit(main())
