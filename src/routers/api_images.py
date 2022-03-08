from typing import List

from bson.binary import Binary
from config.settings import get_settings
from database.mongo import get_database
from docs.router_docs import post as post_responses
from fastapi import Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey
from middleware.api_key import get_api_key
from models.images import (
    PostImageResponseModel,
    PostModelImageInput,
    PostPredictionResponseModel,
)
from motor.motor_asyncio import AsyncIOMotorDatabase
from routers.api_router import APIRouter, CustomApiRoute
from utils.aws import upload_file_to_s3

settings = get_settings()


router = APIRouter(
    tags=["images"],
    route_class=CustomApiRoute,
)


@router.post(
    "/faces",
    summary="Receives a mongo document and insert it.",
    response_model=PostImageResponseModel,
    response_description="Document created .",
    responses=post_responses["create_faces_document"]["responses"],
)
async def create_faces_document(
    files: List[UploadFile] = File(..., example={"files": ("file", ("xxx", "xxxx"))}),
    key: str = Form(..., example={"key": "xxx"}),
    api_key: APIKey = Depends(get_api_key),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> JSONResponse:
    """
    This route does:
      - Receiving a dict that will be inserted in mongo as a document.
    """

    try:
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Could not validate credentials."},
            )
        faces = []
        for f in files:
            file = f.file._file
            faces.append(Binary(file.read(), subtype=128))
        document = {"key": key, "faces": faces}
        inserted = await database["faces"].insert_one(document)
        if inserted.inserted_id is not None:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=post_responses["create_faces_document"]["responses"][200],
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=post_responses["create_faces_document"]["responses"][400],
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": str(e)},
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


@router.post(
    "/predict",
    summary="Get prediction for the image id received.",
    response_model=PostPredictionResponseModel,
    response_description="Sends the prediction processed for the image id.",
    responses=post_responses["prediction"]["responses"],
)
async def predict_image(
    image_id: PostModelImageInput,
    api_key: APIKey = Depends(get_api_key),
    database: AsyncIOMotorDatabase = Depends(get_database),
):  # -> Union[JSONResponse, PostPredictionResponseModel]:
    """
    This route does:
      - Receives an image id.
      - Query MongoDB for the image_id.
      - Sends the mongo object prediction
    """
    try:
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Could not validate credentials."},
            )
        query = {"key": "raw/AQAD4LoxG29XQFFy_3330057.jpg"}
        prediction = await database["predict"].find_one(
            query, {"_id": 0, "predictions": 1}
        )
        if prediction is not None:
            return prediction
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=post_responses["prediction"]["responses"][404],
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": str(e)},
        )
