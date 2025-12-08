# Как написать книгу с помощью проекта

Ниже пошаговый сценарий: от запуска сервиса до получения плана и глав. Все примеры — HTTP-запросы к FastAPI.

## 1. Подготовка
- Требуется Python 3.11+, `pip install -r requirements.txt`.
- По умолчанию `MOCK_LLM=true` — ответы-заглушки, подходят для проверки схемы.
- Для реальной генерации установите Ollama, скачайте модель (например, `mistral`), выставьте `MOCK_LLM=false`, при необходимости задайте `LLM_URL`, `LLM_MODEL`, `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`.
- Запуск сервера:
  ```bash
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
  Документация: `http://localhost:8000/docs`.

## 2. Завести персонажей
Создайте нужных героев через API. Пример `curl`:
```bash
curl -X POST http://localhost:8000/characters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Анна",
    "role": "героиня",
    "traits": "смелая, наблюдательная",
    "background": "археолог",
    "speaking_style": "короткие, точные реплики",
    "private_goals": "найти артефакт"
  }'
```
Повторите для всех ключевых персонажей. Их `id` понадобятся дальше. Список: `GET /characters`.

## 3. Сгенерировать план книги
Вызов `POST /book/plan` с жанром, масштабом текста и id главных героев:
```bash
curl -X POST http://localhost:8000/book/plan \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "приключения",
    "target_length": "10 глав, 70k слов",
    "tone": "динамичный",
    "setting": "альтернативный 1930 год",
    "main_characters": [1, 2]
  }'
```
Ответ содержит `synopsis` и массив `chapters` (номер, название, краткое содержание). Сохраните этот объект — он будет входом для генерации глав.

## 4. Написать главу по плану
Выберите номер главы и активных персонажей. Вызов `POST /book/generate_chapter`:
```bash
curl -X POST http://localhost:8000/book/generate_chapter \
  -H "Content-Type: application/json" \
  -d '{
    "book_plan": {
      "synopsis": "Герои ищут артефакт в альтернативном 1930 году.",
      "chapters": [
        { "number": 1, "title": "Старт экспедиции", "summary": "Команда собирается и получает карту." }
      ]
    },
    "chapter_number": 1,
    "active_characters": [1, 2]
  }'
```
В ответе `chapter_text` — черновик главы. Повторите для каждой главы, подставляя правильный `chapter_number`.

## 5. (Опционально) Сцены и диалоги
- POV-сцена от лица каждого героя: `POST /scene/generate_pov` с `scene_description`, `character_ids`, границами `words_min/words_max`. Ответ: `results` по каждому id.
- Диалог: `POST /scene/generate_dialogue` с `scene_description`, `character_ids`, `turns`. Ответ: общий текст и массив реплик.

## 6. (Опционально) CrewAI POV
Эндпоинт `POST /scene/generate_pov_crewai` собирает POV через CrewAI. Поля:
```json
{
  "scene_description": "Крыша старого города, неон внизу",
  "characters": [
    {"name": "Сорц", "role": "хакер", "traits": "..."},
    {"name": "Лан Кай", "role": "инженер", "traits": "..."}
  ],
  "words_min": 300,
  "words_max": 700
}
```
Ответ сейчас — единый текст. Если нужен отдельный POV для каждого героя, добавьте пост-обработку или разделяйте задачи по персонажам.

## 7. Практический рабочий поток
1) Завести персонажей → 2) Получить их `id` → 3) Сгенерировать план книги → 4) По очереди вызывать генерацию глав, подставляя план и активных героев → 5) При необходимости уточнять сцены/диалоги через сценовые эндпоинты → 6) Собрать результат в редакторе, при необходимости редактировать вручную.

## 8. Советы по качеству
- Реальная модель (Ollama + `MOCK_LLM=false`) даст осмысленный текст; мок-режим — только для отладки схемы.
- Для длинных книг регулируйте `LLM_MAX_TOKENS` и `LLM_TEMPERATURE` в окружении.
- Хранение по умолчанию — SQLite `data.db`; поменять можно `DATABASE_URL`.
