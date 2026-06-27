from app.models.document import Document, DocumentStatus
from app.schemas.document import UploadResponse, DocumentResponse
from app.core.database import SessionLocal
from app.services.parsing_service import parse_pdf, parse_docx, chunk_text
from app.core.elastic import es
from app.core.config import settings
from fastapi import UploadFile, HTTPException
import uuid
from typing import List
import logging

logger = logging.getLogger(__name__)

def process_upload(file: UploadFile) -> UploadResponse:
    content = file.file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 20 MB")
    
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is missing")
    ext = filename.split('.')[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}")
    
    doc_id = uuid.uuid4()
    
    try:
        if ext == "pdf":
            pages = parse_pdf(content)
        elif ext == "docx":
            pages = parse_docx(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
    except Exception as e:
        logger.error(f"Parsing error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse document")
    
    db = SessionLocal()
    document = Document(
        id=doc_id,
        file_name=filename,
        status=DocumentStatus.INDEXING,
        total_pages=len(pages)
    )
    db.add(document)
    db.commit()
    
    chunk_index = 0
    for page_text, page_num in pages:
        chunks = chunk_text(page_text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
        for chunk in chunks:
            chunk_id = f"{doc_id}_{chunk_index}"
            es.index(
                index="documents",
                id=chunk_id,
                body={
                    "id": chunk_id,
                    "document_id": str(doc_id),
                    "file_name": filename,
                    "page_number": page_num,
                    "chunk_id": chunk_id,
                    "text": chunk
                }
            )
            chunk_index += 1
    
    document.status = DocumentStatus.READY
    db.commit()
    db.close()
    
    return UploadResponse(
        document_id=doc_id,
        message="Document uploaded and indexed successfully",
        chunks_indexed=chunk_index
    )

def get_documents() -> List[DocumentResponse]:
    db = SessionLocal()
    docs = db.query(Document).all()
    db.close()
    return [DocumentResponse.from_orm(doc) for doc in docs]