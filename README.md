# University Knowledge Search

Интеллектуальная поисковая система по внутренней базе знаний университета.

## Стек
- Backend: FastAPI, PostgreSQL, Elasticsearch, Redis
- Frontend: React + TypeScript, Vite
- DevOps: Docker, Docker Compose, GitHub Actions
- Тестирование: Pytest, Playwright, Locust

## Запуск
1. Скопируйте `.env.example` в `.env`.
2. Выполните `docker-compose up --build`.
3. Откройте `http://localhost` в браузере.

## Документация API
Swagger UI доступен по адресу `http://localhost:8000/docs`.

## Тестирование
```bash
cd backend
pytest