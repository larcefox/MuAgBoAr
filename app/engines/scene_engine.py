from typing import List
from app.agents import CharacterAgent
from app.models import Character
from app.llm import BaseLLMClient


async def generate_pov_scene(scene_description: str, characters: List[Character], llm_client: BaseLLMClient, words_min=None, words_max=None):
    results = []
    for character in characters:
        agent = CharacterAgent(character, llm_client)
        pov_text = await agent.generate_pov(scene_description, words_min=words_min, words_max=words_max)
        results.append({
            "character_id": character.id,
            "character_name": character.name,
            "pov_text": pov_text,
        })
    return results


async def generate_dialogue_scene(scene_description: str, characters: List[Character], llm_client: BaseLLMClient, turns: int = 3):
    history = ""
    turn_results = []
    for _ in range(turns):
        for character in characters:
            agent = CharacterAgent(character, llm_client)
            reply = await agent.generate_dialogue_reply(scene_description, history)
            utterance = f"{character.name}: {reply.strip()}"
            turn_results.append({
                "character_id": character.id,
                "character_name": character.name,
                "utterance": utterance,
            })
            history += utterance + "\n"
    return history.strip(), turn_results
