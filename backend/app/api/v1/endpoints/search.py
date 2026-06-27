from fastapi import APIRouter, Query
from app.services.search_service import search_documents
from app.schemas.search import SearchResponse

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Results per page")
):
    return search_documents(q, page, size)