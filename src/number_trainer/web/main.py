"""Main entry point for Number Trainer web application."""

import uvicorn
from .app import app


def main():
    """Run the web application."""
    uvicorn.run(
        "src.number_trainer.web.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
