from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    chunk_id: str
    file_name: str
    page: int
    text: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    took: float