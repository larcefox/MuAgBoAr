from typing import Optional
from app.llm import BaseLLMClient
from app.models import Character


class CharacterAgent:
    def __init__(self, character: Character, llm_client: BaseLLMClient):
        self.character = character
        self.llm_client = llm_client

    def _build_backstory(self) -> str:
        parts = [
            f"Name: {self.character.name}",
            f"Role: {self.character.role or 'Unknown'}",
            f"Traits: {self.character.traits or 'N/A'}",
            f"Background: {self.character.background or 'N/A'}",
            f"Speaking style: {self.character.speaking_style or 'Neutral'}",
            f"Private goals: {self.character.private_goals or 'Hidden'}",
        ]
        return "\n".join(parts)

    async def generate_pov(self, scene_description: str, words_min: Optional[int] = None, words_max: Optional[int] = None) -> str:
        backstory = self._build_backstory()
        constraints = ""
        if words_min:
            constraints += f"Minimum words: {words_min}. "
        if words_max:
            constraints += f"Maximum words: {words_max}. "
        prompt = (
            f"You are writing from the first-person perspective of the character below.\n"
            f"Scene: {scene_description}\n"
            f"Character sheet:\n{backstory}\n"
            f"Write vivid prose in Russian. {constraints}"
        )
        return await self.llm_client.generate(prompt)

    async def generate_dialogue_reply(self, scene_description: str, history: str) -> str:
        backstory = self._build_backstory()
        prompt = (
            f"We are writing a dialogue. Respond as the character with 1-2 spoken lines in Russian.\n"
            f"Scene: {scene_description}\n"
            f"Dialogue so far:\n{history}\n"
            f"Character sheet:\n{backstory}\n"
            f"Answer in first person, prefixing with the character name."
        )
        return await self.llm_client.generate(prompt, max_tokens=200)
