import pytest
from unittest.mock import MagicMock, patch
from fastapi import UploadFile
from app.aws import S3Resource


def test_s3_upload_file_success():
    s3_resource = S3Resource()
    file = MagicMock(spec=UploadFile)
    file.filename = "test.jpg"
    with patch.object(s3_resource.s3, "upload_fileobj", return_value=None):
        assert s3_resource.upload_file_to_s3(file, "dog", "cough", "question1") is not None


@pytest.mark.asyncio
async def test_s3_upload_file_failure():
    s3_resource = S3Resource()
    file = MagicMock(spec=UploadFile)
    file.filename = "test.jpg"
    with patch.object(s3_resource.s3, "upload_fileobj", side_effect=Exception):
        assert await s3_resource.upload_file_to_s3(file, "dog", "cough", "question1") is None


@pytest.mark.asyncio
async def test_s3_remove_file_success():
    s3_resource = S3Resource()
    with patch.object(s3_resource.s3, "Object", return_value=MagicMock(delete=MagicMock(return_value=None))):
        assert await s3_resource.remove_file_from_s3(
            "https://vetchat.s3.region.amazonaws.com/dog_cough_question1.jpg") is True


@pytest.mark.asyncio
async def test_s3_remove_file_failure():
    s3_resource = S3Resource()
    with patch.object(s3_resource.s3, "Object", side_effect=Exception):
        assert await s3_resource.remove_file_from_s3(
            "https://vetchat.s3.region.amazonaws.com/dog_cough_question1.jpg") is False
