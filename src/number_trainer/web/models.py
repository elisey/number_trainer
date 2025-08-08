"""Pydantic models for web API."""

from typing import Optional

from pydantic import BaseModel


class ExerciseRequest(BaseModel):
    """Request to create a new exercise."""

    difficulty: int  # 1, 2, or 3 (number of digits)


class ExerciseResponse(BaseModel):
    """Response with exercise data."""

    exercise_id: str
    question: str
    operation: str


class AnswerRequest(BaseModel):
    """Request to check an answer."""

    exercise_id: str
    answer: int
    time_taken: Optional[float] = None


class AnswerResponse(BaseModel):
    """Response after checking an answer."""

    correct: bool
    correct_answer: int
    message: str
    time_taken: Optional[float] = None


class StatsResponse(BaseModel):
    """Statistics response."""

    total_exercises: int
    correct_answers: int
    incorrect_answers: int
    accuracy: float
    average_time: Optional[float] = None
