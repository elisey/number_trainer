"""Tests for web API endpoints."""

from fastapi.testclient import TestClient

from src.number_trainer.web.app import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "number-trainer-web"


def test_root_endpoint():
    """Test root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Number Trainer" in response.text
    assert "text/html" in response.headers["content-type"]


def test_create_exercise():
    """Test creating a new exercise."""
    response = client.post("/api/exercise/new", json={"difficulty": 1})
    assert response.status_code == 200

    data = response.json()
    assert "exercise_id" in data
    assert "question" in data
    assert "operation" in data
    assert len(data["exercise_id"]) > 0


def test_create_exercise_invalid_difficulty():
    """Test creating exercise with invalid difficulty."""
    response = client.post("/api/exercise/new", json={"difficulty": 5})
    assert response.status_code == 400


def test_check_answer_not_found():
    """Test checking answer for non-existent exercise."""
    response = client.post("/api/exercise/check", json={"exercise_id": "non-existent", "answer": 42})
    assert response.status_code == 404


def test_exercise_workflow():
    """Test complete exercise workflow."""
    # Create exercise
    create_response = client.post("/api/exercise/new", json={"difficulty": 1})
    assert create_response.status_code == 200
    exercise = create_response.json()

    # Check answer (we don't know the correct answer, so just test the endpoint)
    check_response = client.post(
        "/api/exercise/check",
        json={
            "exercise_id": exercise["exercise_id"],
            "answer": 999,  # Likely wrong answer
            "time_taken": 5.0,
        },
    )
    assert check_response.status_code == 200

    result = check_response.json()
    assert "correct" in result
    assert "correct_answer" in result
    assert "message" in result
    assert "time_taken" in result


def test_get_stats():
    """Test getting statistics."""
    response = client.get("/api/stats")
    assert response.status_code == 200

    data = response.json()
    assert "total_exercises" in data
    assert "correct_answers" in data
    assert "incorrect_answers" in data
    assert "accuracy" in data
    assert isinstance(data["total_exercises"], int)
    assert isinstance(data["correct_answers"], int)
    assert isinstance(data["incorrect_answers"], int)
    assert isinstance(data["accuracy"], float)
