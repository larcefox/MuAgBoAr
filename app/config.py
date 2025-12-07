import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "book-multiagent-codex"
    llm_backend: str = os.getenv("LLM_BACKEND", "ollama")
    llm_url: str = os.getenv("LLM_URL", "http://localhost:11434")
    llm_model: str = os.getenv("LLM_MODEL", "mistral")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "512"))
    mock_llm: bool = os.getenv("MOCK_LLM", "true").lower() == "true"

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> "Settings":
    return Settings()
