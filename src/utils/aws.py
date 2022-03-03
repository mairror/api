import logging

import boto3


def upload_file_to_s3(
    file,
    bucket,
    s3_folder=None,
    object_name=None,
):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3_folder: Directory or folder to store the file.
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    try:
        s3 = boto3.resource("s3")
        s3_object = s3.Object(bucket, s3_folder + object_name)
        with file as f:
            # response = s3_object.put(Body=f, ChecksumAlgorithm='SHA1')
            response = s3_object.put(Body=f)

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            object_details = {
                "checksum": response["ETag"].replace('"', ""),
                "path": f"s3://{bucket}/{s3_folder}{object_name}",
            }
            return object_details
    except Exception as e:
        logging.error(e.response)
        return False
