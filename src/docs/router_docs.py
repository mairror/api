post = {
    "create_upload_file": {
        "responses": {
            201: {"description": "The object was uploaded successfully."},
            400: {
                "description": "There was a problem uploading the file, check the API logs."
            },
        }
    },
    "create_faces_document": {
        "responses": {
            200: {"description": "The document was inserted successfully."},
            400: {
                "description": "There was an error inserting the document, check the API logs."
            },
        }
    },
}
