import boto3
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "adi-platform-datasets"

def upload_file_to_s3(file):
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}_{file.filename}"

    s3.upload_fileobj(file.file, BUCKET_NAME, file_name)

    return file_name