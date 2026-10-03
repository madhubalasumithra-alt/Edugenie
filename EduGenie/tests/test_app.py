from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa_endpoint_with_mock(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda q: (f"Answer: {q}", "mock", "mock-model"))
    response = client.post("/qa", json={"question": "What is AI?"})
    assert response.status_code == 200
    assert response.json()["provider"] == "mock"


def test_quiz_endpoint_with_mock(monkeypatch):
    from schemas import QuizItem

    items = [
        QuizItem(
            question="2 + 2 = ?",
            options=["1", "2", "3", "4"],
            correct_answer="4",
            explanation="Two plus two equals four.",
        )
    ]
    monkeypatch.setattr(main, "generate_quiz", lambda text, count: (items, "mock", "mock-model"))
    response = client.post("/quiz", json={"text": "Basic arithmetic", "count": 1})
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 1


def test_empty_input_rejected():
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422
