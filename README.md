# 🌟 README.md

Ниже приведён готовый файл `README.md` для размещения в корне репозитория.

```markdown
# 📚 University Knowledge Search

**Интеллектуальная поисковая система по внутренней базе знаний университета**

Система позволяет загружать документы в форматах PDF и DOCX, извлекать из них текст, индексировать его и выполнять полнотекстовый поиск с учётом русской морфологии. Результаты поиска подсвечиваются и сортируются по релевантности.

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)](https://www.elastic.co/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---

## 🚀 Демонстрация

![Демонстрация](https://via.placeholder.com/800x400?text=Search+interface+screenshot)

---

## 📋 Функциональные возможности

- **Загрузка документов**  
  - Drag‑and‑Drop, множественная загрузка.  
  - Поддерживаются PDF и DOCX (макс. 20 МБ).  
  - Отображение прогресса загрузки и индексации.

- **Полнотекстовый поиск**  
  - Русскоязычная морфология (анализатор Elasticsearch).  
  - Нечёткий поиск (fuzziness) для исправления опечаток.  
  - Подсветка совпадений в найденных фрагментах.  
  - Пагинация (по 10 результатов).  
  - Кеширование частых запросов (Redis, TTL 5 минут).

- **Мониторинг**  
  - Сбор метрик через Prometheus.  
  - Визуализация в Grafana.

- **Документация API**  
  - Swagger UI доступен по адресу `/docs`.

---

## 🛠️ Технологический стек

| Компонент       | Технология |
|-----------------|------------|
| **Backend**     | Python 3.10, FastAPI, SQLAlchemy, Pydantic |
| **Frontend**    | React 18, TypeScript, Vite, Axios |
| **База данных** | PostgreSQL 15 |
| **Поиск**       | Elasticsearch 8.11 |
| **Кеш**         | Redis 7 |
| **Контейнеры**  | Docker, Docker Compose |
| **Мониторинг**  | Prometheus, Grafana |
| **Тестирование**| Pytest, Playwright, Locust |
| **CI/CD**       | GitHub Actions |

---

## 📦 Установка и запуск

### Предварительные требования

- Docker (>= 20.10) и Docker Compose (>= 2.0).
- Git.
- (Опционально) Node.js и Python для локальной разработки.

### Шаги

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/your-username/university-knowledge-search.git
   cd university-knowledge-search
   ```

2. **Настройте переменные окружения**
   ```bash
   cp .env.example .env
   # При необходимости отредактируйте .env (пароли, хосты)
   ```

3. **Запустите все сервисы через Docker Compose**
   ```bash
   docker-compose up --build
   ```
   Это поднимет 7 контейнеров: backend, frontend, postgres, elasticsearch, redis, prometheus, grafana.

4. **Создайте индекс в Elasticsearch**  
   *Если автоматическое создание отключено* – выполните команду в новом терминале:
   ```bash
   curl -X PUT "http://localhost:9200/documents" -H "Content-Type: application/json" -d '{
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
   }'
   ```

5. **Откройте приложение в браузере**
   - Фронтенд: [http://localhost](http://localhost)
   - Документация API: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Grafana: [http://localhost:3000](http://localhost:3000) (логин `admin`, пароль `admin`)

---

## 📖 Использование

### Загрузка документов
1. На главной странице перетащите файлы (PDF/DOCX) в область Drag‑and‑Drop или выберите через диалог.
2. Наблюдайте за прогрессом загрузки и индексации.
3. После завершения документ появится в списке «Uploaded Documents».

### Поиск
1. Введите запрос в поле поиска.
2. Нажмите кнопку «Найти» или Enter.
3. Результаты отобразятся карточками с подсветкой совпадений и релевантностью.
4. Используйте пагинацию для просмотра всех результатов.

### API
Все эндпоинты задокументированы через Swagger (`/docs`). Основные:
- `POST /api/v1/documents/upload` – загрузить файл.
- `GET /api/v1/documents/documents` – список загруженных документов.
- `GET /api/v1/search?q={query}` – поиск.

---

## 🧪 Тестирование

### Юнит-тесты (бэкенд)
```bash
cd backend
pip install -r requirements.txt
pytest --cov=app --cov-report=html
```

### E2E-тесты (Playwright)
```bash
cd e2e-tests
npm install
npm test
```

### Нагрузочные тесты (Locust)
```bash
locust -f locustfile.py --host http://localhost:8000
```
Откройте `http://localhost:8089`, задайте количество пользователей и запустите.

---

## 📁 Структура проекта

```
.
├── backend/                 # Бэкенд (FastAPI)
│   ├── app/
│   │   ├── api/             # Роутеры и эндпоинты
│   │   ├── core/            # Конфигурация, подключения к БД/ES/Redis
│   │   ├── models/          # SQLAlchemy модели
│   │   ├── schemas/         # Pydantic схемы
│   │   ├── services/        # Бизнес-логика
│   │   └── utils/           # Вспомогательные модули (кеш)
│   ├── tests/               # Тесты (pytest)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Фронтенд (React + Vite)
│   ├── src/
│   │   ├── components/      # UI-компоненты
│   │   ├── services/        # API-клиент
│   │   └── types/           # TypeScript-типы
│   ├── public/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── e2e-tests/               # Сквозные тесты Playwright
├── scripts/                 # Вспомогательные скрипты
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🤝 Участие в разработке

1. Форкните репозиторий.
2. Создайте ветку для вашей фичи (`git checkout -b feature/amazing-feature`).
3. Закоммитьте изменения (`git commit -m 'Add some amazing feature'`).
4. Отправьте в ваш форк (`git push origin feature/amazing-feature`).
5. Откройте Pull Request.

---

## 📄 Лицензия

Распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

---

## 🙏 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/) – за отличный фреймворк.
- [Elasticsearch](https://www.elastic.co/) – за мощный поисковый движок.
- [React](https://reactjs.org/) – за удобный UI.
- Всем преподавателям и участникам учебной практики.

---

**Сделано с ❤️ для Университета**
```