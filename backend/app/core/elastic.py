from elasticsearch import Elasticsearch
from app.core.config import settings

es = Elasticsearch([settings.ELASTICSEARCH_URL])

def create_index_if_not_exists():
    index_name = "documents"
    if not es.indices.exists(index=index_name):
        body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "russian_analyzer": {
                            "type": "russian",
                            "stopwords": "_russian_"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "document_id": {"type": "keyword"},
                    "file_name": {"type": "text", "analyzer": "russian_analyzer"},
                    "page_number": {"type": "integer"},
                    "chunk_id": {"type": "keyword"},
                    "text": {"type": "text", "analyzer": "russian_analyzer"}
                }
            }
        }
        es.indices.create(index=index_name, body=body)