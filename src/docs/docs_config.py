from typing import Any

from pydantic import BaseSettings


class DocsSettings(BaseSettings):
    license_name: str = "MIT"
    license_url: str = "https://github.com/mairror/api/blob/main/LICENSE"
    logo_url: str = (
        "https://raw.githubusercontent.com/mairror/api/main/docs/images/logo.png"
    )
    title: str = "Mairror API"
    version: str = "0.1.0"
    email: str = "dev@aacecan.com,blopezp@protonmail.com"
    repo_url: str = "https://github.com/mairror/api/blob/main/README.md"
    description: str = """
# Mairror API

This is an API that acts as a central point for managing all events that occur within the Mairror project.

## What can be done with this API

You can make the following operations with this API:#/images/create_upload_file_images_upload_post

- Receiving a new image from a Telegram bot or an Streamlit frontend
- Send back those images to the source
- Send the image to an AWS S3 bucket
- Insert image's metadata and data into MongoDB
- Send and receive eventes to an AMQP broker

## Operation responses from the API

All the requests will throw:

- Request duration
- Response duration
- Response headers
"""
    terms_of_service: str = "Terms of service"
    tags_metadata: Any = [
        {
            "name": "info",
            "description": "Endpoint to test and print debug information about the API.",
            "externalDocs": {
                "description": "Code",
                "url": "https://github.com/mairror/api/routers/api_info.py",
            },
        },
        {
            "name": "images",
            "description": "Endpoint to perform operations with images",
            "externalDocs": {
                "description": "Code",
                "url": "https://github.com/mairror/api/routers/api_images.py",
            },
        },
    ]
