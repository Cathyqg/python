import boto3
from app.settings import settings
from uuid import uuid4

class S3Service:
    def __init__(self):
        self.bucket = settings.s3_bucket
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    def upload_file(self, filename, file_content):
        key = f"uploads/{uuid4()}_{filename}"
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=file_content)
        return f"s3://{self.bucket}/{key}" 