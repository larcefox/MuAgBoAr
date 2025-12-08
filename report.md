# CrewAI POV тест (Сорц и Лан)

- Окружение: активировал `.venv`.
- Команда запуска:
  ```bash
  . .venv/bin/activate && python - <<'PY'
  from app.scenes.crewai_scenes import build_pov_scene_crew
  from app.crewai.characters_crewai import get_test_characters

  scene = "Крыша старого города, опутанная проводами. Ночь, дрожащий неон внизу."
  chars = get_test_characters()
  crew = build_pov_scene_crew(chars, scene, words_min=150, words_max=250)
  result = crew.kickoff()
  print("--- RESULT START ---")
  print(result)
  print("--- RESULT END ---")
  PY
  ```
- Ключевые параметры: 2 тестовых персонажа (`get_test_characters`), сцена — крыша старого города, лимит 150–250 слов на POV.
- Результат (сжатие): вернулся одиночный блок текста в первом лице, описывает крыши, неон и поиск проекта «Геликс»; финальная строка от имени Лан Кай. (Ollama сгенерировал единый ответ; разбиения по персонажам нет — текущее поведение CrewAI/Task приводит к слитию.)
- Итог: запрос обработан без ошибок; для раздельных POV по персонажам потребуется пост-обработка `result` или использование отдельных задач/агентов с явным сбором выходов.

## 2025-12-07 — CrewAI POV (русский язык)
- Изменил промпт/бекстори агентов: добавлено требование отвечать только на русском (`app/crewai/characters_crewai.py`, `app/scenes/crewai_scenes.py`).
- Тест:
  ```bash
  . .venv/bin/activate && python - <<'PY'
  from app.scenes.crewai_scenes import build_pov_scene_crew
  from app.crewai.characters_crewai import get_test_characters
  scene = "Крыша старого города, опутанная проводами. Ночь, дрожащий неон внизу."
  crew = build_pov_scene_crew(get_test_characters(), scene, words_min=80, words_max=120)
  result = crew.kickoff()
  print(result)
  PY
  ```
- Результат: текст пришёл на русском (первое лицо, без примесей английского). Ответ всё ещё единым блоком (поведение CrewAI, задачи сливаются). Если нужен отдельный POV по каждому герою — потребуется пост-обработка или отдельный сбор результатов по таскам.
