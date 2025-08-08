"""Tests for web API models."""

import pytest
from pydantic import ValidationError

from src.number_trainer.web.models import (
    AnswerRequest,
    AnswerResponse,
    ExerciseRequest,
    ExerciseResponse,
    StatsResponse,
)


def test_exercise_request_valid():
    """Test valid exercise request."""
    request = ExerciseRequest(difficulty=2)
    assert request.difficulty == 2


def test_exercise_request_invalid():
    """Test invalid exercise request."""
    with pytest.raises(ValidationError):
        ExerciseRequest(difficulty="invalid")


def test_exercise_response():
    """Test exercise response model."""
    response = ExerciseResponse(
        exercise_id="test-id", question="2 + 3", operation="addition"
    )
    assert response.exercise_id == "test-id"
    assert response.question == "2 + 3"
    assert response.operation == "addition"


def test_answer_request():
    """Test answer request model."""
    request = AnswerRequest(exercise_id="test-id", answer=5, time_taken=2.5)
    assert request.exercise_id == "test-id"
    assert request.answer == 5
    assert request.time_taken == 2.5


def test_answer_request_without_time():
    """Test answer request without time."""
    request = AnswerRequest(exercise_id="test-id", answer=5)
    assert request.time_taken is None


def test_answer_response():
    """Test answer response model."""
    response = AnswerResponse(
        correct=True, correct_answer=5, message="Правильно!", time_taken=2.5
    )
    assert response.correct is True
    assert response.correct_answer == 5
    assert response.message == "Правильно!"
    assert response.time_taken == 2.5


def test_stats_response():
    """Test stats response model."""
    response = StatsResponse(
        total_exercises=10,
        correct_answers=8,
        incorrect_answers=2,
        accuracy=80.0,
        average_time=3.5,
    )
    assert response.total_exercises == 10
    assert response.correct_answers == 8
    assert response.incorrect_answers == 2
    assert response.accuracy == 80.0
    assert response.average_time == 3.5
