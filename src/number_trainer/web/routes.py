"""API routes for Number Trainer web interface."""

import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

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


@router.get("/sw.js", response_class=HTMLResponse)
async def service_worker() -> HTMLResponse:
    """Serve service worker from root for PWA requirements."""
    from pathlib import Path

    sw_path = Path(__file__).parent / "static" / "sw.js"

    if sw_path.exists():
        with open(sw_path) as f:
            return HTMLResponse(content=f.read(), media_type="application/javascript")
    else:
        return HTMLResponse(content="// Service worker not found", status_code=404)


@router.get("/favicon.ico", response_model=None)
async def favicon() -> FileResponse | HTMLResponse:
    """Serve favicon from root."""
    from pathlib import Path

    # Try to serve SVG as favicon, fallback to PNG
    svg_path = Path(__file__).parent / "static" / "icons" / "math_training_icon.svg"
    if svg_path.exists():
        return FileResponse(str(svg_path), media_type="image/svg+xml")

    return HTMLResponse(content="", status_code=404)


@router.get("/apple-touch-icon.png", response_model=None)
@router.get("/apple-touch-icon-precomposed.png", response_model=None)
@router.get("/apple-touch-icon-120x120.png", response_model=None)
@router.get("/apple-touch-icon-120x120-precomposed.png", response_model=None)
@router.get("/apple-touch-icon-152x152.png", response_model=None)
@router.get("/apple-touch-icon-180x180.png", response_model=None)
async def apple_touch_icon() -> FileResponse | HTMLResponse:
    """Serve Apple touch icons."""
    from pathlib import Path

    # Try to serve the appropriate Apple touch icon
    icons_dir = Path(__file__).parent / "static" / "icons"

    # Look for the best matching icon sizes for Apple devices
    for icon_name in ["icon-152.png", "icon-144.png", "icon-192.png", "math_training_icon.svg"]:
        icon_path = icons_dir / icon_name
        if icon_path.exists():
            media_type = "image/svg+xml" if icon_name.endswith(".svg") else "image/png"
            return FileResponse(str(icon_path), media_type=media_type)

    return HTMLResponse(content="", status_code=404)


@router.get("/", response_class=HTMLResponse)
async def read_root() -> str:
    """Serve the main HTML page."""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Number Trainer</title>

        <!-- PWA Meta Tags -->
        <meta name="description" content="Mathematical exercise training app for practicing arithmetic">
        <meta name="theme-color" content="#2563eb">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="NumTrainer">
        <meta name="format-detection" content="telephone=no">

        <!-- PWA Manifest -->
        <link rel="manifest" href="/static/manifest.json">

        <!-- Favicon and Icons -->
        <link rel="icon" type="image/svg+xml" href="/static/icons/math_training_icon.svg">
        <link rel="apple-touch-icon" href="/static/icons/math_training_icon.svg">

        <!-- Stylesheets -->
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
                        <input type="number" id="answer-input" placeholder="Enter answer"
                               inputmode="numeric" pattern="[0-9]*" autofocus>
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

        <!-- Service Worker Registration -->
        <script>
        // Register service worker for PWA functionality
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', async () => {
                try {
                    const registration = await navigator.serviceWorker.register('/sw.js');
                    console.log('SW registered successfully:', registration.scope);

                    // Handle updates
                    registration.addEventListener('updatefound', () => {
                        console.log('SW update found');
                    });
                } catch (error) {
                    console.log('SW registration failed:', error);
                }
            });
        }
        </script>
    </body>
    </html>
    """
