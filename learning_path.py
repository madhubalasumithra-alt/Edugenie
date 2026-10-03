from ai_client import GeminiService


def get_learning_recommendations(topic: str, level: str = "auto") -> tuple[str, str, str]:
    service = GeminiService()
    prompt = f"""
Create a practical learning path for the topic: {topic}
Learner level: {level}

Structure the answer as:
1. Goal
2. Prerequisites
3. Beginner stage
4. Intermediate stage
5. Advanced stage
6. Practice/project ideas
7. Suggested resource TYPES (for example: official docs, textbook chapters, practice sites, videos)
8. A realistic 4-week study schedule

Keep the progression step-by-step. Do not invent specific links or certifications.
""".strip()
    result = service.generate_text(prompt, temperature=0.35, max_output_tokens=1800)
    return result, "gemini", service.model
