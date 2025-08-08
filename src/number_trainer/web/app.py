"""FastAPI application for Number Trainer web interface."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router

# Get the path to static files
static_path = Path(__file__).parent / "static"

app = FastAPI(
    title="Number Trainer Web",
    description="Web interface for Number Trainer application",
    version="0.1.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include API routes
app.include_router(router)
