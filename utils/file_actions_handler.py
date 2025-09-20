import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import datetime
from django.conf import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_BUCKET_REGION,
)


def upload_file_to_s3(file, file_name):
    """
    Uploads a file to S3.

    Args:
        file: The file object to upload.
        file_name: The name to save the file as in the bucket.

    Returns:
        The public URL of the uploaded file.
    """
    try:
        # print("file", file.dict())
        key = file_name
        s3_client.upload_fileobj(
            file,
            settings.AWS_BUCKET_NAME,
            key,
            ExtraArgs={'ContentType': file.content_type},  # ExtraArgs={'ACL': 'public-read'}
        )

        print("file uploaded successfully")
        print(f"{settings.AWS_S3__BUCKET_BASE_URL}{key}")

        return f"{settings.AWS_S3__BUCKET_BASE_URL}{key}"

    except (NoCredentialsError, PartialCredentialsError) as e:
        raise ValueError(f"Failed to upload file: {e}") from e


def get_file_url_from_s3(file_key):
    """
    Generates a pre-signed URL for retrieving a file from S3.

    Args:
        file_key: The key of the file in the S3 bucket.

    Returns:
        A pre-signed URL.
    """
    try:
        return s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_key},
            ExpiresIn=3600,  # URL expires in 1 hour
        )
    except Exception as e:
        raise ValueError(f"Failed to generate pre-signed URL: {e}") from e


def get_public_file_url(file_key):
    """
    Constructs the public URL for a file in S3 (assuming public access is allowed).

    Args:
        file_key: The key of the file in the S3 bucket.

    Returns:
        The public URL of the file.
    """
    return f"{settings.AWS_S3__BUCKET_BASE_URL}{file_key}"
