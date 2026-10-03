from typing import Literal

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=20_000)


class QuizRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)
    count: int = Field(default=3, ge=1, le=10)


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=5000)
    level: Literal["beginner", "intermediate", "advanced", "auto"] = "auto"


class TextResponse(BaseModel):
    result: str
    provider: str
    model: str | None = None


class QuizItem(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizItem]
    provider: str
    model: str | None = None


class GenericTaskRequest(BaseModel):
    task: Literal["qa", "explain", "quiz", "summarize", "learn"]
    text: str = Field(min_length=1, max_length=20_000)
    level: Literal["beginner", "intermediate", "advanced", "auto"] = "auto"
