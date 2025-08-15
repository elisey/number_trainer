"""API routes for Number Trainer web interface."""

import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from ..core.models import Operation
from ..core.trainer import MathTrainer
from .models import (
    AnswerRequest,
    AnswerResponse,
    ExerciseRequest,
    ExerciseResponse,
    StatsResponse,
)

# Global trainers for different difficulties and active exercises storage
trainers: dict[int, MathTrainer] = {
    1: MathTrainer(min_digits=1, max_digits=1),
    2: MathTrainer(min_digits=2, max_digits=2),
    3: MathTrainer(min_digits=3, max_digits=3),
}
active_exercises: dict[str, tuple] = {}  # exercise_id -> (exercise, trainer)

router = APIRouter()


@router.post("/api/exercise/new", response_model=ExerciseResponse)
async def create_exercise(request: ExerciseRequest) -> ExerciseResponse:
    """Create a new exercise based on difficulty."""
    if request.difficulty not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Difficulty must be 1, 2, or 3")

    # Get trainer for the requested difficulty
    trainer = trainers[request.difficulty]
    exercise = trainer.generate_exercise()

    exercise_id = str(uuid.uuid4())
    active_exercises[exercise_id] = (exercise, trainer)

    # Format operation symbol for display
    op_symbols = {Operation.ADDITION: "+", Operation.SUBTRACTION: "-"}

    return ExerciseResponse(
        exercise_id=exercise_id,
        question=f"{exercise.first_number} {op_symbols[exercise.operation]} {exercise.second_number}",
        operation=exercise.operation.value,
    )


@router.post("/api/exercise/check", response_model=AnswerResponse)
async def check_answer(request: AnswerRequest) -> AnswerResponse:
    """Check the answer for an exercise."""
    if request.exercise_id not in active_exercises:
        raise HTTPException(status_code=404, detail="Exercise not found")

    exercise, trainer = active_exercises[request.exercise_id]

    # Check answer using trainer
    result = trainer.check_answer(exercise, request.answer, request.time_taken or 0.0)

    # Clean up the exercise
    del active_exercises[request.exercise_id]

    return AnswerResponse(
        correct=result.is_correct,
        correct_answer=result.correct_answer,
        message=result.message,
        time_taken=result.time_taken,
    )


@router.get("/api/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    """Get current statistics."""
    # Aggregate stats from all trainers
    total_stats = {
        "total_exercises": 0,
        "correct_answers": 0,
        "incorrect_answers": 0,
        "accuracy": 0.0,
    }

    for trainer in trainers.values():
        trainer_stats = trainer.get_stats()
        total_stats["total_exercises"] += trainer_stats["total_exercises"]
        total_stats["correct_answers"] += trainer_stats["correct_answers"]
        total_stats["incorrect_answers"] += trainer_stats["incorrect_answers"]

    # Calculate overall accuracy
    if total_stats["total_exercises"] > 0:
        total_stats["accuracy"] = round((total_stats["correct_answers"] / total_stats["total_exercises"]) * 100, 1)

    return StatsResponse(
        total_exercises=int(total_stats["total_exercises"]),
        correct_answers=int(total_stats["correct_answers"]),
        incorrect_answers=int(total_stats["incorrect_answers"]),
        accuracy=total_stats["accuracy"],
        average_time=None,  # Not tracking average time across trainers for now
    )


@router.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "number-trainer-web"}


@router.get("/", response_class=HTMLResponse)
async def read_root() -> str:
    """Serve the main HTML page."""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Number Trainer</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <div id="app">
            <div class="container">
                <h1>Number Trainer</h1>
                <div id="welcome-screen" class="screen">
                    <div class="card">
                        <h2>Select Difficulty</h2>
                        <div class="difficulty-buttons">
                            <button class="btn btn-primary" onclick="startTraining(1)">
                                1 digit
                                <div class="btn-subtitle">Numbers 1-9</div>
                            </button>
                            <button class="btn btn-primary" onclick="startTraining(2)">
                                2 digits
                                <div class="btn-subtitle">Numbers 10-99</div>
                            </button>
                            <button class="btn btn-primary" onclick="startTraining(3)">
                                3 digits
                                <div class="btn-subtitle">Numbers 100-999</div>
                            </button>
                        </div>
                    </div>
                </div>

                <div id="exercise-screen" class="screen hidden">
                    <div class="card">
                        <div id="question" class="question"></div>
                        <input type="number" id="answer-input" placeholder="Enter answer" autofocus>
                        <div class="button-group">
                            <button class="btn btn-success" onclick="checkAnswer()">Check</button>
                            <button class="btn btn-secondary" onclick="showWelcome()">Main Menu</button>
                        </div>
                    </div>
                </div>

                <div id="result-screen" class="screen hidden">
                    <div class="card">
                        <div id="result-message" class="result-message"></div>
                        <div id="result-details" class="result-details"></div>
                        <div class="button-group">
                            <button class="btn btn-primary" onclick="nextExercise()">Next Exercise</button>
                            <button class="btn btn-secondary" onclick="showWelcome()">Main Menu</button>
                        </div>
                    </div>
                </div>

                <div id="stats-panel" class="stats-panel">
                    <div class="stats-item">
                        <span class="stats-label">Total:</span>
                        <span id="stats-total">0</span>
                    </div>
                    <div class="stats-item">
                        <span class="stats-label">Correct:</span>
                        <span id="stats-correct">0</span>
                    </div>
                    <div class="stats-item">
                        <span class="stats-label">Incorrect:</span>
                        <span id="stats-incorrect">0</span>
                    </div>
                    <div class="stats-item">
                        <span class="stats-label">Accuracy:</span>
                        <span id="stats-accuracy">0%</span>
                    </div>
                </div>
            </div>
        </div>
        <script src="/static/js/app.js"></script>
    </body>
    </html>
    """
