import boto3
import os

from typing import Optional
from fastapi import UploadFile
from pydantic import HttpUrl

from app.utils import format_file_name


class S3Resource:
    def __init__(self):
        self.resource = boto3.resource('s3')
        self.bucket_name = 'vetchat'
        self.aws_region = os.getenv('AWS_DEFAULT_REGION')
        self.s3 = self.resource.Bucket(self.bucket_name)

    async def upload_file_to_s3(self, file: UploadFile, animal: str, symptom: str, question: str) -> Optional[HttpUrl]:
        """Uploads a file to S3 and returns the URL of the uploaded file."""
        file_extension = file.filename.split(".")[-1]

        animal = format_file_name(animal)
        symptom = format_file_name(symptom)
        question = format_file_name(question)

        file_key = f"{animal}_{symptom}_{question}.{file_extension}"

        try:
            response = self.s3.upload_fileobj(
                Fileobj=file.file,
                Key=file_key
            )

            file_url = f"https://{self.bucket_name}.s3.{self.aws_region}.amazonaws.com/{file_key}"
            return file_url

        except Exception as e:
            return None
