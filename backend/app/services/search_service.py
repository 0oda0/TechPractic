from app.core.elastic import es
from app.core.config import settings
from app.utils.cache import get_cache, set_cache
from app.schemas.search import SearchResponse, SearchResult
from fastapi import HTTPException
import time
import logging

logger = logging.getLogger(__name__)

def search_documents(query: str, page: int = 1, size: int = 10) -> SearchResponse:
    cache_key = f"search:{query}:{page}:{size}"
    cached = get_cache(cache_key)
    if cached:
        logger.info(f"Returning cached results for query: {query}")
        return SearchResponse(**cached)
    
    start_time = time.time()
    try:
        from_ = (page - 1) * size
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["text", "file_name"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            },
            "from": from_,
            "size": size,
            "highlight": {
                "fields": {
                    "text": {
                        "fragment_size": 150,
                        "number_of_fragments": 1,
                        "pre_tags": ["<mark>"],
                        "post_tags": ["</mark>"]
                    }
                }
            }
        }
        response = es.search(index="documents", body=body)
        
        results = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            highlight = hit.get('highlight', {})
            text = highlight.get('text', [source.get('text', '')])[0] if highlight else source.get('text', '')
            results.append(SearchResult(
                chunk_id=source['chunk_id'],
                file_name=source['file_name'],
                page=source['page_number'],
                text=text,
                score=hit['_score']
            ))
        
        total = response['hits']['total']['value']
        took = (time.time() - start_time) * 1000
        
        search_resp = SearchResponse(results=results, total=total, took=took)
        set_cache(cache_key, search_resp.dict(), ttl=settings.CACHE_TTL)
        return search_resp
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")