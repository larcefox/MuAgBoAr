from crewai import Agent
from app.core.llm_client import CrewOllamaLLM

llm = CrewOllamaLLM()  # будет использовать mistral по умолчанию


def create_character_agent(char: dict) -> Agent:
    """
    char — словарь с ключами:
    name, role, traits, background, speaking_style, private_goals
    """
    name = char["name"]
    role = char.get("role", "персонаж истории")
    traits = char.get("traits", "")
    background = char.get("background", "")
    speaking_style = char.get("speaking_style", "")
    private_goals = char.get("private_goals", "")

    backstory = (
        f"Ты — персонаж по имени {name}. "
        f"Роль: {role}. Характер: {traits}. "
        f"Биография: {background}. "
        f"Стиль речи: {speaking_style}. "
        f"Скрытые цели: {private_goals}. "
        "Ты всегда отвечаешь от первого лица, художественным стилем, "
        "сохраняя голос и характер персонажа. Не выходи из роли. "
        "Отвечай только на русском языке."
    )

    agent = Agent(
        role=f"Персонаж: {name}",
        goal=f"Выражать мысли, действия и речь персонажа {name} в истории.",
        backstory=backstory,
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
    return agent


def get_test_characters():
    sorc = {
        "name": "Сорц",
        "role": "хакер",
        "traits": "замкнутый, язвительный, параноидально осторожный",
        "background": "Вырос в технограде, взламывал системы распределения ресурсов...",
        "speaking_style": "сухой техно-арго, короткие фразы, сарказм",
        "private_goals": "найти доказательства проекта 'Геликс'",
    }
    lan = {
        "name": "Лан Кай",
        "role": "инженер-сборщик",
        "traits": "тёплый, болтливый, смышлёный",
        "background": "Вырос в нижних секторах мегаполиса, чинит всё из подручных деталей...",
        "speaking_style": "живая, быстрая речь, много шуток и аналогий",
        "private_goals": "открыть свой техно-бокс и не дать Сорцу угробить себя",
    }
    return [sorc, lan]
