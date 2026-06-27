from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.document_service import process_upload, get_documents
from app.schemas.document import UploadResponse, DocumentResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_document(file: UploadFile = File(...)):
    return process_upload(file)

@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents():
    return get_documents()