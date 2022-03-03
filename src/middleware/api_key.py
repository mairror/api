from config.settings import get_settings
from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

settings = get_settings()


def get_api_key(
    api_key_header: str = Security(
        APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)
    )
) -> str:
    """
    This function checks the header and his value for correct authentication if not a
    403 error is returned:
      - api_key_header = Security api header

    https://github.com/tiangolo/fastapi/issues/142
    """
    if api_key_header == settings.API_KEY:
        return api_key_header
