# book-multiagent-codex

Локальная мультиагентная система для написания книг на базе FastAPI и Python.

## Возможности
- CRUD для персонажей (характер, биография, стиль речи и цели).
- Генерация сцен в режимах POV и диалога на базе локальной LLM (Ollama или мок-режим).
- Генерация плана книги и текста главы.
- Авто-документация Swagger/OpenAPI.

## Быстрый старт
1. Создайте виртуальное окружение и установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. (Опционально) Установите и запустите Ollama, скачайте модель (например, mistral).
3. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Откройте документацию по адресу `http://localhost:8000/docs`.

### Переменные окружения
- `DATABASE_URL` — строка подключения к БД (по умолчанию SQLite `sqlite:///./data.db`).
- `LLM_URL` — адрес Ollama (`http://localhost:11434`).
- `LLM_MODEL` — имя модели (по умолчанию `mistral`).
- `LLM_TEMPERATURE`, `LLM_MAX_TOKENS` — параметры генерации.
- `MOCK_LLM` — включить мок-ответы (по умолчанию `true` для простого запуска без модели).

### Пример запуска с реальной моделью
```bash
export MOCK_LLM=false
uvicorn app.main:app --reload
```

### Структура API
- `GET /health` — проверка состояния сервиса.
- `POST /characters` — создание персонажа, `GET /characters` — список, `GET/PUT/DELETE /characters/{id}` — операции над конкретным персонажем.
- `POST /scene/generate_pov` — POV-сцена.
- `POST /scene/generate_dialogue` — диалог.
- `POST /book/plan` — план книги.
- `POST /book/generate_chapter` — генерация главы.
