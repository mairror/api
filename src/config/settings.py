import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    RELOAD: bool = True if os.getenv("ENVIRONMENT") == "development" else False
    MAX_CONNECTIONS_COUNT: int = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
    MIN_CONNECTIONS_COUNT: int = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
    WEB_CONCURRENCY: int = int(os.getenv("WEB_CONCURRENCY", 10))
    OPENAPI_URL: str = os.getenv("OPENAPI_URL", "/openapi.json")
    DOCS_URL: str = os.getenv("DOCS_URL", "/documentation")
    REDOC_URL: str = os.getenv("REDOC_URL", "/redoc")
    S3_BUCKET_RAW_NAME: str = os.getenv("S3_BUCKET_RAW_NAME", "mairror-test")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "mairror")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    VERSION: str = os.getenv("VERSION", "0.0.0")

    class Config:
        if os.path.exists(".env"):
            env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
