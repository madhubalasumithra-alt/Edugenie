from ai_client import GeminiService


def summarize_text(text: str) -> tuple[str, str, str]:
    service = GeminiService()
    prompt = f"""
Summarize the educational passage below for revision.
Keep the central facts and reasoning, remove repetition, and use concise bullet points when useful.
Do not add information that is not supported by the passage.

PASSAGE:
{text}
""".strip()
    result = service.generate_text(prompt, temperature=0.15, max_output_tokens=1000)
    return result, "gemini", service.model
