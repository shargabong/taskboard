import os
from pathlib import Path

os.environ["TASKBOARD_DATABASE_URL"] = "sqlite:///./data/test_taskboard.db"
os.environ["TASKBOARD_SECRET_KEY"] = "test-secret"
os.environ["TASKBOARD_SEED_DEMO"] = "true"
os.environ["TASKBOARD_SESSION_HTTPS_ONLY"] = "false"

Path("data/test_taskboard.db").unlink(missing_ok=True)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def login(client: TestClient, email: str, password: str):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )
