from config.settings import get_settings
from docs.docs_config import DocsSettings
from fastapi.openapi.utils import get_openapi

settings = get_settings()
docs_settings = DocsSettings()


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=docs_settings.title,
        version=docs_settings.version,
        description=docs_settings.description,
        tags=docs_settings.tags_metadata,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": docs_settings.logo_url}
    openapi_schema["info"] = {
        "title": docs_settings.title,
        "version": docs_settings.version,
        "description": docs_settings.description,
        "termsOfService": docs_settings.terms_of_service,
        "contact": {
            "name": "Get Help with this API",
            "url": docs_settings.repo_url,
            "email": docs_settings.email,
        },
        "license": {
            "name": docs_settings.license_name,
            "url": docs_settings.license_url,
        },
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
