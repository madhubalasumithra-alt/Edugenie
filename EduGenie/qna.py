from ai_client import GeminiService


def answer_question(question: str) -> tuple[str, str, str]:
    service = GeminiService()
    prompt = f"""
You are EduGenie, a careful educational assistant.
Answer the student's question accurately and clearly.
Use simple wording first, then add necessary detail.
If the question is ambiguous, state the assumption you are making.
Do not invent citations or claim to have checked sources you did not access.

Student question:
{question}
""".strip()
    result = service.generate_text(prompt, temperature=0.25, max_output_tokens=1200)
    return result, "gemini", service.model
