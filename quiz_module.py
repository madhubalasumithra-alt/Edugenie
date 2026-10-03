from pydantic import BaseModel, Field

from ai_client import GeminiService
from schemas import QuizItem


class _QuizEnvelope(BaseModel):
    questions: list[QuizItem] = Field(min_length=1, max_length=10)


def generate_quiz(text: str, count: int = 3) -> tuple[list[QuizItem], str, str]:
    service = GeminiService()
    prompt = f"""
Create exactly {count} multiple-choice questions from the learning material below.
Each question must have exactly 4 distinct options.
The correct_answer must exactly match one of the four option strings.
Add a short explanation of why the answer is correct.
Use only information supported by the material.

LEARNING MATERIAL:
{text}
""".strip()

    quiz = service.generate_structured(
        prompt,
        _QuizEnvelope,
        temperature=0.2,
        max_output_tokens=2200,
    )

    if len(quiz.questions) != count:
        raise RuntimeError(
            f"Expected {count} quiz questions but the model returned {len(quiz.questions)}. Please try again."
        )

    for item in quiz.questions:
        if item.correct_answer not in item.options:
            raise RuntimeError("Quiz validation failed: a correct answer was not present in its options.")

    return quiz.questions, "gemini", service.model
