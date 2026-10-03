from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai_client import AIConfigurationError
from config import get_settings
from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    GenericTaskRequest,
    LearningPathRequest,
    QuestionRequest,
    QuizRequest,
    QuizResponse,
    TextRequest,
    TextResponse,
)
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Google Gemini powered learning assistant",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _clean(value: str) -> str:
    text = value.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Input cannot be empty.")
    if len(text) > settings.max_input_chars:
        raise HTTPException(
            status_code=413,
            detail=f"Input is too long. Maximum is {settings.max_input_chars} characters.",
        )
    return text


def _error(exc: Exception) -> HTTPException:
    if isinstance(exc, HTTPException):
        return exc
    if isinstance(exc, AIConfigurationError):
        return HTTPException(status_code=503, detail=str(exc))
    return HTTPException(status_code=500, detail=f"EduGenie could not complete the request: {exc}")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
        "explainer_provider": settings.explainer_provider,
    }


@app.post("/qa", response_model=TextResponse)
def qa(payload: QuestionRequest):
    try:
        result, provider, model = answer_question(_clean(payload.question))
        return TextResponse(result=result, provider=provider, model=model)
    except Exception as exc:
        raise _error(exc) from exc


@app.post("/explain", response_model=TextResponse)
def explain(payload: TextRequest):
    try:
        result, provider, model = explain_concept(_clean(payload.text))
        return TextResponse(result=result, provider=provider, model=model)
    except Exception as exc:
        raise _error(exc) from exc


@app.post("/quiz", response_model=QuizResponse)
def quiz(payload: QuizRequest):
    try:
        questions, provider, model = generate_quiz(_clean(payload.text), payload.count)
        return QuizResponse(questions=questions, provider=provider, model=model)
    except Exception as exc:
        raise _error(exc) from exc


@app.post("/summarize", response_model=TextResponse)
def summarize(payload: TextRequest):
    try:
        result, provider, model = summarize_text(_clean(payload.text))
        return TextResponse(result=result, provider=provider, model=model)
    except Exception as exc:
        raise _error(exc) from exc


@app.post("/learn/recommendations", response_model=TextResponse)
def learn(payload: LearningPathRequest):
    try:
        result, provider, model = get_learning_recommendations(
            _clean(payload.topic), payload.level
        )
        return TextResponse(result=result, provider=provider, model=model)
    except Exception as exc:
        raise _error(exc) from exc


@app.post("/api/run")
def run_task(payload: GenericTaskRequest):
    """Convenience endpoint used by the single-page frontend."""
    text = _clean(payload.text)
    try:
        if payload.task == "qa":
            result, provider, model = answer_question(text)
            return TextResponse(result=result, provider=provider, model=model)
        if payload.task == "explain":
            result, provider, model = explain_concept(text)
            return TextResponse(result=result, provider=provider, model=model)
        if payload.task == "summarize":
            result, provider, model = summarize_text(text)
            return TextResponse(result=result, provider=provider, model=model)
        if payload.task == "learn":
            result, provider, model = get_learning_recommendations(text, payload.level)
            return TextResponse(result=result, provider=provider, model=model)
        if payload.task == "quiz":
            questions, provider, model = generate_quiz(text, 3)
            return QuizResponse(questions=questions, provider=provider, model=model)
        raise HTTPException(status_code=400, detail="Unsupported task.")
    except Exception as exc:
        raise _error(exc) from exc
