from typing import Any, Dict, Optional

from pydantic import BaseModel


class PostModel(BaseModel):
    pass


class PostImageModel(PostModel):
    pass
    # https://stackoverflow.com/questions/60127234/how-to-use-a-pydantic-model-with-form-data-in-fastapi
    # https://github.com/tiangolo/fastapi/issues/2387
    # https://stackoverflow.com/questions/65504438/how-to-add-both-file-and-json-body-in-a-fastapi-post-request
    # https://github.com/tiangolo/fastapi/issues/657#issuecomment-623385604
    # https://fastapi.tiangolo.com/tutorial/schema-extra-example/#field-additional-arguments
    # https://github.com/tiangolo/fastapi/issues/1442

    # source: str = Form(...)


class PostResponseModel(BaseModel):
    pass


class PostImageResponseModel(PostResponseModel):
    pass


class PostFaceModel(PostModel):
    key: str
    faces: Optional[Dict[str, Any]]
