import os
import requests
from crewai.llms.base_llm import BaseLLM
from crewai.events.types.llm_events import LLMCallType

LLM_URL = os.getenv("LLM_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")


class LLMClient:
    def __init__(self, model: str = None, timeout: int = 120):
        self.model = model or LLM_MODEL
        self.url = f"{LLM_URL}/api/generate"
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        response = requests.post(self.url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")


class CrewOllamaLLM(BaseLLM):
    """
    Нативная реализация BaseLLM для CrewAI поверх локального Ollama.
    """

    is_litellm = False

    def __init__(self, model: str = None, temperature: float | None = None, **kwargs):
        model_name = model or LLM_MODEL
        super().__init__(model=model_name, temperature=temperature, provider="ollama", **kwargs)
        self.client = LLMClient(model=model_name)

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ):
        formatted = self._format_messages(messages)
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in formatted])

        self._emit_call_started_event(
            messages=formatted,
            tools=tools,
            callbacks=callbacks,
            available_functions=available_functions,
            from_task=from_task,
            from_agent=from_agent,
        )

        try:
            raw_response = self.client.generate(prompt)
            response = self._apply_stop_words(raw_response)
            response = self._validate_structured_output(response, response_model)

            self._emit_call_completed_event(
                response=response,
                call_type=LLMCallType.LLM_CALL,
                from_task=from_task,
                from_agent=from_agent,
                messages=formatted,
            )
            return response

        except Exception as exc:  # noqa: BLE001
            self._emit_call_failed_event(error=str(exc), from_task=from_task, from_agent=from_agent)
            raise
