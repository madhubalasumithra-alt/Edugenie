from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_env: str = "development"
    debug: bool = True

    # Google Gemini configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    # Explanation provider: "gemini" (default) or "local"
    explainer_provider: str = "gemini"
    local_model_name: str = "MBZUAI/LaMini-Flan-T5-783M"
    local_max_new_tokens: int = 220

    # Limits keep requests responsive and reduce accidental oversized prompts.
    max_input_chars: int = 20_000

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
