from typing import List
from crewai import Task, Crew
from app.crewai.characters_crewai import create_character_agent


def build_pov_scene_crew(characters: List[dict], scene_description: str, words_min: int = 300, words_max: int = 700) -> Crew:
    agents = [create_character_agent(c) for c in characters]
    tasks = []

    for agent in agents:
        name = agent.role.replace("Персонаж: ", "")
        description = (
            f"Сцена: {scene_description}\n\n"
            f"Напиши, как персонаж {name} воспринимает и проживает эту сцену. "
            f"Текст от первого лица, {words_min}–{words_max} слов, "
            "с внутренними переживаниями, ощущениями, краткими деталями окружения. "
            "Сохраняй характер и стиль персонажа. "
            "Ответ должен быть на русском языке."
        )

        task = Task(
            description=description,
            agent=agent,
            expected_output=f"Художественный текст сцены от лица персонажа {name}.",
        )
        tasks.append(task)

    crew = Crew(
        agents=agents,
        tasks=tasks,
    )
    return crew


if __name__ == "__main__":
    from app.crewai.characters_crewai import get_test_characters

    chars = get_test_characters()
    scene = "Крыша старого города, опутанная проводами. Ночь, дрожащий неон внизу."
    crew = build_pov_scene_crew(chars, scene)
    result = crew.kickoff()
    print(result)
