from pydantic import BaseModel, UUID4
from datetime import datetime
from enum import Enum

class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    INDEXING = "indexing"
    READY = "ready"
    ERROR = "error"

class DocumentBase(BaseModel):
    file_name: str
    status: DocumentStatus
    upload_date: datetime
    total_pages: int

class DocumentResponse(DocumentBase):
    id: UUID4
    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    document_id: UUID4
    message: str
    chunks_indexed: int