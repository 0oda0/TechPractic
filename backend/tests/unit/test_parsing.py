import pytest
from app.services.parsing_service import chunk_text

def test_chunk_text():
    text = "a" * 2500
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    assert len(chunks) == 3
    assert chunks[0] == "a" * 1000
    assert chunks[1] == "a" * 1000
    assert chunks[2] == "a" * 500