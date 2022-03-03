# Mairror API

The Mairror API

## Testing the image upload

- Not authorized

```bash
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@shakil.jpg" -F "source=streamlit" http://127.0.0.1:8000/images/upload
```

- Authorized

```bash
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@shakil.jpg" -F "source=streamlit" http://127.0.0.1:8000/images/upload
```

## Converting Anaconda environment to pip requirements

1. Use [conda-minify](https://github.com/jamespreed/conda-minify) to export only the top level requirements without the build string. It **must** be installed and executed within the conda `base` environment.

conda run --name base conda-minify -n mairror-api > environment.yml

2. Use the conversion tool `utils/conversor.py` to convert the requirements to a pip requirements file. It reads the previously generated YAML file and outputs a requirements.txt file in the same folder.

python utils/conversor.py

## Resources

- [python-multipart](https://andrew-d.github.io/python-multipart/)
- [S3 boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html)
- [FastAPI cURL](https://stackoverflow.com/questions/68981869/how-to-upload-a-single-file-to-fastapi-server-using-curl)
- [FastAPI custom request handlers](https://fastapi.tiangolo.com/advanced/custom-request-and-route/)
- [OpenAPI Specification extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions)
- [OpenAPI exclude](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#exclude-from-openapi)
- [FastAPI Request Files](https://fastapi.tiangolo.com/tutorial/request-files/)
