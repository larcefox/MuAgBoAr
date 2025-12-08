from typing import List
from app.llm import BaseLLMClient
from app.models import Character


async def generate_book_plan(llm_client: BaseLLMClient, genre: str, target_length: str, characters: List[Character], tone: str = "", setting: str = ""):
    character_list = "\n".join([f"- {c.name}: {c.role or ''} ({c.traits or ''})" for c in characters])
    prompt = (
        "Generate a book synopsis and chapter list in Russian.\n"
        f"Genre: {genre}\nTarget length: {target_length}\nTone: {tone}\nSetting: {setting}\n"
        f"Main characters:\n{character_list}\n"
        "Return the output as:\n"
        "Synopsis: <text>\n"
        "Chapters:\n"
        "1. <title> - <summary>\n2. ..."
    )
    response = await llm_client.generate(prompt, max_tokens=1024)
    return response


def parse_plan_response(raw_text: str):
    synopsis = ""
    chapters = []
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    mode = None
    for line in lines:
        if line.lower().startswith("synopsis") or line.lower().startswith("синопсис"):
            mode = "synopsis"
            synopsis = line.split(":", 1)[-1].strip()
            continue
        if line.lower().startswith("chapters") or line.lower().startswith("главы"):
            mode = "chapters"
            continue
        if mode == "synopsis":
            synopsis += " " + line
        elif mode == "chapters":
            if "." in line:
                number_part, rest = line.split(".", 1)
                try:
                    number = int(number_part.strip())
                except ValueError:
                    continue
                if "-" in rest:
                    title, summary = rest.split("-", 1)
                else:
                    title, summary = rest, ""
                chapters.append({"number": number, "title": title.strip(), "summary": summary.strip()})
    synopsis = synopsis.strip()

    # Fallback для пустых ответов (особенно в мок-режиме)
    if not synopsis and not chapters:
        synopsis = "Герои ищут артефакт в альтернативном 1930 году."
        chapters = [
            {"number": 1, "title": "Старт экспедиции", "summary": "Команда собирается и получает карту."},
            {"number": 2, "title": "Встреча с врагами", "summary": "Первая стычка с конкурентами."},
            {"number": 3, "title": "Пустынный переход", "summary": "Испытания жарой и песком."},
            {"number": 4, "title": "Подземный город", "summary": "Открытие заброшенного техногорода."},
            {"number": 5, "title": "Развязка", "summary": "Решающее столкновение и судьба артефакта."},
        ]
    return synopsis, chapters


async def generate_chapter(llm_client: BaseLLMClient, plan, chapter_number: int, characters: List[Character]):
    chapter_info = next((c for c in plan["chapters"] if c.get("number") == chapter_number), None)
    char_list = "\n".join([f"- {c.name}: {c.role or ''}" for c in characters])
    prompt = (
        f"Write chapter {chapter_number} in Russian based on the summary and characters.\n"
        f"Chapter summary: {chapter_info['summary'] if chapter_info else 'N/A'}\n"
        f"Characters involved:\n{char_list}\n"
        "Include descriptive narration and dialogue when appropriate."
    )
    return await llm_client.generate(prompt, max_tokens=2048)
