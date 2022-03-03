# from routers.eda import router as eda_router
import sentry_sdk
import uvicorn
from config.settings import get_settings
from docs.open_api import custom_openapi
from fastapi import FastAPI, HTTPException, status
from routers.api_images import router as api_images_router
from routers.api_info import router as api_info_router
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

settings = get_settings()


def create_application() -> FastAPI:
    app = FastAPI(
        swagger_ui_parameters={
            "syntaxHighlight.theme": "obsidian",
            "dom_id": "#swagger-ui",
            "layout": "BaseLayout",
            "deepLinking": True,
            "showExtensions": True,
            "showCommonExtensions": True,
        },
        openapi_url=settings.OPENAPI_URL,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
    )
    app.include_router(api_info_router, prefix="/info", tags=["info"])
    app.include_router(api_images_router, prefix="/images", tags=["images"])
    app.router.redirect_slashes = False

    return app


app = create_application()

custom_openapi(app)

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        release=settings.VERSION,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0,
    )
    try:
        app.add_middleware(SentryAsgiMiddleware)
    except Exception:
        # pass silently if the Sentry integration failed
        pass


@app.on_event("startup")
async def startup():
    if settings.DEBUG:
        print(settings)


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown")


@app.get("/")
async def root():
    return {"message": "success!"}


# Calling this endpoint to see if the setup works.
# If yes, an error message will show in Sentry dashboard
@app.get("/sentry")
async def sentry():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Test sentry integration"},
    )


if __name__ == "__main__":
    # https://www.uvicorn.org/settings/
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        log_level=settings.LOG_LEVEL,
        workers=settings.WEB_CONCURRENCY,
        reload=settings.RELOAD,
    )
