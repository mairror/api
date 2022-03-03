from config.settings import get_settings
from database.mongo import get_database
from docs.router_docs import post as post_responses
from fastapi import Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey
from middleware.api_key import get_api_key
from models.images import PostImageResponseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from routers.api_router import APIRouter, CustomApiRoute
from utils.aws import upload_file_to_s3

settings = get_settings()


router = APIRouter(
    tags=["images"],
    route_class=CustomApiRoute,
)


@router.post(
    "/upload",
    summary="Receives a new image and process it",
    response_model=PostImageResponseModel,
    response_description="Receives a new image and process it",
    responses=post_responses["create_upload_file"]["responses"],
)
async def create_upload_file(
    api_key: APIKey = Depends(get_api_key),
    source: str = Form(..., example={"source": "streamlit"}),
    file: UploadFile = File(
        ...,
        description="The file to be uploaded, as multipart/form-data",
        example={"file": "@image.jpg"},
    ),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> JSONResponse:
    """
    This route does:
      - Receiving an image from a source (Telegram/Streamlit)
      - Uploads it to S3
      - Updates MongoDB
    """
    try:
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Could not validate credentials."},
            )
        object_details = upload_file_to_s3(
            file.file._file, settings.S3_BUCKET_RAW_NAME, "raw/", file.filename
        )
        if object_details:
            object_details["source"] = source
            inserted = await database["raw"].insert_one(object_details)
            if inserted.inserted_id is not None:
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content=post_responses["create_upload_file"]["responses"][201],
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=post_responses["create_upload_file"]["responses"][400],
                )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": str(e)},
        )
