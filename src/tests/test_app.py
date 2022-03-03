import pytest
from config.settings import get_settings
from httpx import AsyncClient
from main import app

settings = get_settings()


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        app=app, base_url="http://{settings.HOST}:{settings.PORT}"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "success!"}


@pytest.mark.anyio
async def test_sentry():
    async with AsyncClient(
        app=app, base_url="http://{settings.HOST}:{settings.PORT}"
    ) as ac:
        response = await ac.get("/sentry")
    assert response.status_code == 404
    assert response.json() == {"detail": {"message": "Test sentry integration"}}
