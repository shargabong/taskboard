from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TaskBoard"
    environment: str = "development"
    debug: bool = False
    secret_key: str = "dev-secret-change-me"
    database_url: str = "sqlite:///./data/taskboard.db"
    session_cookie: str = "taskboard_session"
    session_https_only: bool = False
    seed_demo: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TASKBOARD_",
        extra="ignore",
    )

    @property
    def sqlalchemy_url(self) -> str:
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
