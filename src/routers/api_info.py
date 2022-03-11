from config.settings import get_settings
from fastapi.responses import JSONResponse
from routers.api_router import APIRouter, CustomApiRoute

settings = get_settings()

router = APIRouter(
    tags=["info"],
    route_class=CustomApiRoute,
)


@router.get(
    "/",
    summary="Test the API status",
    response_description="Test API connectivity.",
    responses={
        200: {
            "description": "The API is up and running.",
        },
    },
)
async def root() -> JSONResponse:
    """
    This endpoints is only for testing purposes.

    It returns a message when the API is ready to serve requests.
    """
    return JSONResponse(
        status_code=200,
        content={"message": "Welcome to the Mairror API!"},
    )


@router.get(
    "/variables",
    summary="Get the API variables",
    response_description="Test API variables.",
    responses={
        200: {
            "description": "Return variables configured at runtime.",
        },
    },
)
async def info() -> JSONResponse:
    """
    This endpoint returns information about the application setup parameters

    - DEBUG
    - ENVIRONMENT
    - MAX_CONNECTIONS_COUNT
    - MIN_CONNECTIONS_COUNT
    """
    return JSONResponse(
        status_code=200,
        content={
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
        },
    )
