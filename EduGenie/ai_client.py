from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from config import get_settings


T = TypeVar("T", bound=BaseModel)


class AIConfigurationError(RuntimeError):
    pass


class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.model = self.settings.gemini_model

        if not self.settings.gemini_api_key:
            raise AIConfigurationError(
                "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your key."
            )

        try:
            from google import genai
        except ImportError as exc:
            raise AIConfigurationError(
                "The Google GenAI SDK is not installed. Run: pip install -r requirements.txt"
            ) from exc

        self._genai = genai
        self.client = genai.Client(api_key=self.settings.gemini_api_key)

    def _config(self, **kwargs):
        from google.genai import types
        return types.GenerateContentConfig(**kwargs)

    def generate_text(
        self,
        prompt: str,
        *,
        temperature: float = 0.3,
        max_output_tokens: int = 1200,
    ) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=self._config(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text

    def generate_structured(
        self,
        prompt: str,
        schema: type[T],
        *,
        temperature: float = 0.2,
        max_output_tokens: int = 1800,
    ) -> T:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=self._config(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )

        parsed = getattr(response, "parsed", None)
        if isinstance(parsed, schema):
            return parsed
        if isinstance(parsed, dict):
            return schema.model_validate(parsed)

        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty structured response.")
        return schema.model_validate_json(text)
