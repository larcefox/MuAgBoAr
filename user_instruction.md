# Инструкция пользователя

Локальный сервис для генерации плана книги, глав и сцен на базе FastAPI. Ниже — минимальные шаги для запуска и примеры запросов.

## Подготовка окружения
- Требуется Python 3.11+ и pip.
- Установите зависимости: `pip install -r requirements.txt`.
- (Опционально) создайте `.env` рядом с проектом для своих настроек окружения.

## Переменные окружения
- `DATABASE_URL` — БД (по умолчанию SQLite `sqlite:///./data.db`).
- `SERVER_HOST`, `SERVER_PORT` — адрес и порт Uvicorn (по умолчанию `0.0.0.0:8000`).
- `MOCK_LLM` — `true` для мок-ответов без реальной LLM (значение по умолчанию).
- `LLM_URL`, `LLM_MODEL`, `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, `LLM_BACKEND` — параметры Ollama; нужны, если `MOCK_LLM=false`.

## Запуск сервера
```bash
uvicorn app.main:app --reload --host ${SERVER_HOST:-0.0.0.0} --port ${SERVER_PORT:-8000}
```
Проверка готовности: `curl http://localhost:8000/health` или откройте Swagger по адресу `http://localhost:8000/docs`.

## Основные сценарии API
Все запросы — JSON.

### 1) Работа с персонажами
- Создать: `POST /characters`
  ```json
  {
    "name": "Анна",
    "role": "героиня",
    "traits": "храбрая, любознательная",
    "background": "археолог",
    "speaking_style": "короткие, точные реплики",
    "private_goals": "найти артефакт"
  }
  ```
- Список: `GET /characters`
- Получить/обновить/удалить: `GET|PUT|DELETE /characters/{id}`

### 2) Генерация сцен
- POV-сцена: `POST /scene/generate_pov`
  ```json
  {
    "scene_description": "Ночной рынок в пустыне, начинаются торги",
    "character_ids": [1, 2],
    "words_min": 150,
    "words_max": 220
  }
  ```
  Ответ: `results` — массив текстов по каждому персонажу.
- Диалог: `POST /scene/generate_dialogue`
  ```json
  {
    "scene_description": "Спор о цене артефакта",
    "character_ids": [1, 2],
    "turns": 3
  }
  ```
  Ответ: полное поле `dialogue_text` и список реплик `turns`.

### 3) План книги и главы
- План: `POST /book/plan`
  ```json
  {
    "genre": "Приключения",
    "target_length": "10 глав, 70k слов",
    "tone": "динамичный",
    "setting": "альтернативный 1930 год",
    "main_characters": [1, 2]
  }
  ```
  Ответ: `synopsis` и массив `chapters` с номером, названием и кратким содержанием.
- Генерация главы: `POST /book/generate_chapter`
  ```json
  {
    "book_plan": {
      "synopsis": "...",
      "chapters": [{ "number": 1, "title": "Биржа песков", "summary": "..." }]
    },
    "chapter_number": 1,
    "active_characters": [1, 2]
  }
  ```
  Ответ: `chapter_text`.

## Подсказки по режимам LLM
- Быстрый старт: оставьте `MOCK_LLM=true` — ответы будут заглушками, но сервис и схема API проверяются.
- Реальная генерация: установите Ollama, скачайте модель (например, `mistral`), выставьте `MOCK_LLM=false` и задайте `LLM_URL`, `LLM_MODEL`.

## Хранение данных
- По умолчанию используется файл `data.db` в корне проекта (SQLite). Переключить на внешнюю БД можно через `DATABASE_URL`.
