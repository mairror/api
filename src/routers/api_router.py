import time
from typing import Any, Callable

from fastapi import APIRouter as FastAPIRouter
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute
from fastapi.types import DecoratedCallable


class APIRouter(FastAPIRouter):
    """
    Decorates FastAPI's APIRouter.api_route method to add a trailing slash to the
    path. /upload/ -> /upload
    """

    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]
        add_path = super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )
        alternate_path = path + "/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs
        )

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            add_alternate_path(func)
            return add_path(func)

        return decorator


class CustomApiRoute(APIRoute):
    """
    Decorates FastAPI APIRoute in the logs the execution time of any route that inherits
    from this class.
    If an exception occurs, the Request instance will still be in scope,
    so we can read and make use of the request body when handling the error.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                before = time.time()
                response: Response = await original_route_handler(request)
                duration = time.time() - before
                response.headers["X-Response-Time"] = str(duration)
                print(f"route duration: {duration}")
                print(f"route response: {response}")
                print(f"route response headers: {response.headers}")
                return response
            except Exception as e:
                body = await request.body()
                detail = {"errors": e.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler
