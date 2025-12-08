import logging
from typing import Any, Dict
import httpx
from app.config import get_settings

logger = logging.getLogger(__name__)


class BaseLLMClient:
    async def generate(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError


class OllamaClient(BaseLLMClient):
    def __init__(self, base_url: str, model: str, temperature: float = 0.7, max_tokens: int = 512):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            },
        }
        url = f"{self.base_url}/api/generate"
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                logger.error("LLM request failed: %s", exc)
                raise

            try:
                data = response.json()
                return data.get("response", "")
            except Exception:
                return response.text


class MockLLMClient(BaseLLMClient):
    async def generate(self, prompt: str, **kwargs: Any) -> str:
        # Специализированные мок-ответы для стабильных результатов в тестах/документации.
        if "Generate a book synopsis" in prompt:
            return (
                "Synopsis: Герои ищут артефакт в альтернативном 1930 году.\n"
                "Chapters:\n"
                "1. Старт экспедиции - Команда собирается и получает карту.\n"
                "2. Встреча с врагами - Первая стычка с конкурентами.\n"
                "3. Пустынный переход - Испытания жарой и песком.\n"
                "4. Подземный город - Открытие заброшенного техногорода.\n"
                "5. Развязка - Решающее столкновение и судьба артефакта."
            )
        if "Write chapter" in prompt:
            return (
                "Глава описывает подготовку команды, их сомнения и первые шаги к цели. "
                "Диалоги показывают динамику отношений и намечают конфликт с конкурентами."
            )
        return kwargs.get("mock_text") or "[MOCK RESPONSE] " + prompt[:200]


def get_llm_client() -> BaseLLMClient:
    settings = get_settings()
    if settings.mock_llm:
        return MockLLMClient()
    return OllamaClient(
        base_url=settings.llm_url,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )
