import pytest
from config.settings import get_settings
from httpx import AsyncClient
from main import app

settings = get_settings()


@pytest.mark.anyio
async def test_info_root():
    async with AsyncClient(
        app=app, base_url="http://{settings.HOST}:{settings.PORT}"
    ) as ac:
        response = await ac.get("/info")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Mairror API!"}


@pytest.mark.anyio
async def test_info_variables():
    async with AsyncClient(
        app=app, base_url="http://{settings.HOST}:{settings.PORT}"
    ) as ac:
        response = await ac.get("/info/variables")
    assert response.status_code == 200
    assert response.json() == {
        "host": settings.HOST,
        "port": settings.PORT,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
        "environment": settings.ENVIRONMENT,
        "reload": settings.RELOAD,
        "max_connections_count": settings.MAX_CONNECTIONS_COUNT,
        "min_connections_count": settings.MIN_CONNECTIONS_COUNT,
        "web_concurrency": settings.WEB_CONCURRENCY,
        "openapi_url": settings.OPENAPI_URL,
        "docs_url": settings.DOCS_URL,
        "redoc_url": settings.REDOC_URL,
        "version": settings.VERSION,
    }
