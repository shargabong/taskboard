import os
import statistics
import sys
import time

import httpx

BASE_URL = os.getenv("TASKBOARD_BASE_URL", "http://127.0.0.1:8000")
TIMEOUT = 15.0


def timed(client: httpx.Client, method: str, url: str, **kwargs):
    start = time.perf_counter()
    response = client.request(method, url, **kwargs)
    elapsed = (time.perf_counter() - start) * 1000
    return response, elapsed


def login(client: httpx.Client, email: str, password: str) -> None:
    response = client.post(
        "/login",
        data={"email": email, "password": password},
    )
    if response.status_code != 200 or "Сводка" not in response.text:
        raise RuntimeError(f"Не удалось войти как {email}: {response.status_code}")


def percentile(values: list[float], percent: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * percent / 100))
    return ordered[index]


def run_checks() -> list[tuple[str, int, float]]:
    results: list[tuple[str, int, float]] = []
    with httpx.Client(base_url=BASE_URL, timeout=TIMEOUT, follow_redirects=True) as client:
        response, elapsed = timed(client, "GET", "/health")
        results.append(("GET /health", response.status_code, elapsed))
        if response.status_code != 200:
            raise RuntimeError("healthcheck не прошёл")

        response, elapsed = timed(client, "GET", "/login")
        results.append(("GET /login", response.status_code, elapsed))

        login(client, "manager@taskboard.local", "manager123")
        title = f"Smoke task {int(time.time())}"
        response, elapsed = timed(
            client,
            "POST",
            "/tasks/new",
            data={
                "title": title,
                "description": "Проверка основного сценария через HTTP.",
                "priority": "high",
                "assignee_id": "",
            },
        )
        results.append(("POST /tasks/new", response.status_code, elapsed))
        if response.status_code != 200 or title not in response.text:
            raise RuntimeError("задача не создалась")
        task_url = str(response.url)

        response, elapsed = timed(
            client,
            "POST",
            f"{task_url}/comment",
            data={"body": "Комментарий из smoke-теста."},
        )
        results.append(("POST /tasks/{id}/comment", response.status_code, elapsed))
        if response.status_code != 200 or "Комментарий из smoke-теста" not in response.text:
            raise RuntimeError("комментарий не добавился")

        for status in ("in_progress", "done"):
            response, elapsed = timed(
                client,
                "POST",
                f"{task_url}/status",
                data={"new_status": status},
            )
            results.append((f"POST /tasks/{{id}}/status {status}", response.status_code, elapsed))
            if response.status_code != 200:
                raise RuntimeError(f"статус {status} не применился")

        response, elapsed = timed(client, "GET", "/tasks")
        results.append(("GET /tasks", response.status_code, elapsed))

    with httpx.Client(base_url=BASE_URL, timeout=TIMEOUT, follow_redirects=True) as admin:
        login(admin, "admin@taskboard.local", "admin123")
        for path in ("/", "/tasks", "/admin/users"):
            response, elapsed = timed(admin, "GET", path)
            results.append((f"GET {path}", response.status_code, elapsed))
            if response.status_code != 200:
                raise RuntimeError(f"{path} вернул {response.status_code}")
    return results


def run_performance() -> dict[str, list[float]]:
    measurements: dict[str, list[float]] = {}
    with httpx.Client(base_url=BASE_URL, timeout=TIMEOUT, follow_redirects=True) as client:
        measurements["GET /health"] = [
            timed(client, "GET", "/health")[1] for _ in range(50)
        ]
        measurements["GET /login"] = [
            timed(client, "GET", "/login")[1] for _ in range(30)
        ]
        login(client, "admin@taskboard.local", "admin123")
        measurements["GET /tasks"] = [
            timed(client, "GET", "/tasks")[1] for _ in range(30)
        ]
    return measurements


def print_table(rows: list[tuple[str, int, float]]) -> None:
    print("\nФУНКЦИОНАЛЬНЫЕ ПРОВЕРКИ")
    print(f"{'Запрос':45} {'Код':>5} {'Время, мс':>12}")
    print("-" * 66)
    for name, code, elapsed in rows:
        print(f"{name:45} {code:5d} {elapsed:12.1f}")


def print_performance(measurements: dict[str, list[float]]) -> None:
    print("\nЗАМЕРЫ ПРОИЗВОДИТЕЛЬНОСТИ")
    print(f"{'Запрос':20} {'N':>4} {'min':>8} {'avg':>8} {'p95':>8} {'max':>8}")
    print("-" * 62)
    for name, values in measurements.items():
        print(
            f"{name:20} {len(values):4d} "
            f"{min(values):8.1f} {statistics.mean(values):8.1f} "
            f"{percentile(values, 95):8.1f} {max(values):8.1f}"
        )


def main() -> int:
    try:
        results = run_checks()
        print_table(results)
        measurements = run_performance()
        print_performance(measurements)
    except Exception as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print("\nRESULT: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
