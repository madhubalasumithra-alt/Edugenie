from __future__ import annotations

from functools import lru_cache

from config import get_settings


def _gemini_explanation(topic: str) -> tuple[str, str, str]:
    from ai_client import GeminiService

    service = GeminiService()
    prompt = f"""
Explain the following concept to a student in simple, beginner-friendly language:
{topic}

Use this structure:
- Simple definition
- Step-by-step explanation
- One easy example
- Key points to remember
Avoid unnecessary jargon. If jargon is required, define it.
""".strip()
    result = service.generate_text(prompt, temperature=0.25, max_output_tokens=1200)
    return result, "gemini", service.model


@lru_cache(maxsize=1)
def _get_local_pipeline():
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explainer dependencies are not installed. Run: pip install -r requirements-local.txt"
        ) from exc

    settings = get_settings()
    return pipeline(
        "text2text-generation",
        model=settings.local_model_name,
        tokenizer=settings.local_model_name,
    )


def _local_explanation(topic: str) -> tuple[str, str, str]:
    settings = get_settings()
    generator = _get_local_pipeline()
    prompt = (
        "Explain this concept in simple language for a beginner. "
        "Give a short definition, a step-by-step explanation, and one example: "
        f"{topic}"
    )
    output = generator(
        prompt,
        max_new_tokens=settings.local_max_new_tokens,
        do_sample=False,
        truncation=True,
    )
    text = output[0]["generated_text"].strip()
    return text, "local", settings.local_model_name


def explain_concept(topic: str) -> tuple[str, str, str]:
    settings = get_settings()
    provider = settings.explainer_provider.lower().strip()
    if provider == "local":
        return _local_explanation(topic)
    return _gemini_explanation(topic)
