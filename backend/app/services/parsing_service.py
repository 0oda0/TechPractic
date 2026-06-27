import pdfplumber
from docx import Document as DocxDocument
import io
from typing import List, Tuple

def parse_pdf(file_content: bytes) -> List[Tuple[str, int]]:
    pages = []
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append((text, i))
    return pages

def parse_docx(file_content: bytes) -> List[Tuple[str, int]]:
    doc = DocxDocument(io.BytesIO(file_content))
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return [(full_text, 1)]

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
        if start >= len(text):
            break
    return chunks