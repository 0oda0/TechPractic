import pytest
from fastapi import UploadFile
from io import BytesIO
from app.services.document_service import process_upload
from app.core.config import settings

def test_upload_too_large():
    content = b"x" * (settings.MAX_FILE_SIZE + 1)
    file = UploadFile(filename="test.pdf", file=BytesIO(content))
    with pytest.raises(Exception) as excinfo:
        process_upload(file)
    assert "exceeds" in str(excinfo.value)

def test_upload_unsupported_format():
    content = b"some content"
    file = UploadFile(filename="test.txt", file=BytesIO(content))
    with pytest.raises(Exception) as excinfo:
        process_upload(file)
    assert "Unsupported" in str(excinfo.value)