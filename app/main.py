import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlmodel import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.db import create_db_and_tables, engine
from app.routers import admin, auth, tasks
from app.seed import seed_demo_data
from app.web import render

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    for attempt in range(1, 11):
        try:
            create_db_and_tables()
            if settings.seed_demo:
                with Session(engine) as session:
                    seed_demo_data(session)
            break
        except Exception:
            if attempt == 10:
                raise
            logger.warning("Database is not ready, attempt %s/10", attempt)
            time.sleep(2)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie=settings.session_cookie,
    same_site="lax",
    https_only=settings.session_https_only,
)
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "static")),
    name="static",
)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(admin.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code in (403, 404):
        return render(
            request,
            "error.html",
            {"code": exc.status_code, "message": str(exc.detail)},
            status_code=exc.status_code,
        )
    return JSONResponse(
        {"detail": exc.detail},
        status_code=exc.status_code,
        headers=getattr(exc, "headers", None),
    )


@app.get("/health")
def health():
    try:
        with Session(engine) as session:
            session.connection().execute(text("SELECT 1"))
    except Exception:
        return JSONResponse({"status": "error"}, status_code=503)
    return {"status": "ok", "environment": settings.environment}
