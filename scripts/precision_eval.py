"""
Скрипт для оценки качества поиска (Precision@3).
Запускается вручную после развёртывания системы.
"""
import requests
import json

# Эталонные запросы и ожидаемые документы (ID или названия)
QUERIES = [
    {"q": "искусственный интеллект", "expected": ["лекция1.pdf"]},
    # ...
]

def evaluate():
    results = []
    for item in QUERIES:
        q = item["q"]
        resp = requests.get(f"http://localhost:8000/api/v1/search?q={q}&size=3")
        data = resp.json()
        top3 = [r["file_name"] for r in data["results"]]
        expected = item["expected"]
        relevant = sum(1 for doc in expected if doc in top3)
        precision = relevant / len(expected) if expected else 0
        results.append({"query": q, "precision_at_3": precision, "top3": top3})
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    evaluate()