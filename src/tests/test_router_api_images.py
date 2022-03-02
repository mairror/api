# from main import app

# import pytest
# import io
# from httpx import AsyncClient
# from fastapi import status

# from config.settings import get_settings

# settings = get_settings()


# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(app=app, base_url="http://{settings.HOST}:{settings.PORT}") as ac:
#         response = await ac.post(
#             "/images/upload",
#             data={"source": "streamlit"},
#             files={"file": io.BytesIO(b"<file content>")}
#         )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json() == {"description": "The object was uploaded successfully."}

# @pytest.mark.anyio
# async def test_routes_api_images_upload(test_client: AsyncClient):
#     response = await test_client.post(
#         "/images/upload",
#         data={"source": "streamlit"},
#         files={"file": io.BytesIO(b"<file content>")}
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json() == {"description": "The object was uploaded successfully."}


# @pytest.mark.anyio
# async def test_sentry():
#     async with AsyncClient(app=app, base_url="http://{settings.HOST}:{settings.PORT}") as ac:
#         response = await ac.get("/sentry")
#     assert response.status_code == 404
#     assert response.json() == {"detail": {"message": "Test sentry integration"}}
