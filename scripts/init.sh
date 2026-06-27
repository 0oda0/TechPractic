#!/bin/bash
set -e

API_URL="http://localhost:8000/api/v1/documents/upload"
mkdir -p ./temp_pdfs

# Список открытых PDF-лекций (замените на реальные ссылки)
PDF_URLS=(
  "https://example.com/lecture1.pdf"
  "https://example.com/lecture2.pdf"
)

for url in "${PDF_URLS[@]}"; do
  filename=$(basename "$url")
  echo "Downloading $filename..."
  curl -L -o "./temp_pdfs/$filename" "$url"
  echo "Uploading $filename..."
  curl -X POST "$API_URL" -F "file=@./temp_pdfs/$filename"
  echo ""
done

rm -rf ./temp_pdfs
echo "All done."