"""Production entry point for Number Trainer web application."""

import os
import uvicorn


def main() -> None:
    """Run the web application in production mode."""
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))

    # Production settings
    uvicorn.run(
        "src.number_trainer.web.app:app",
        host=host,
        port=port,
        workers=workers,
        reload=False,  # Disable reload in production
        log_level=os.getenv("LOG_LEVEL", "info"),
        access_log=True,
        server_header=False,  # Security: don't expose server info
        date_header=False,  # Security: don't expose date info
        forwarded_allow_ips="*",  # Allow forwarded headers
        proxy_headers=True,  # Trust proxy headers
    )


if __name__ == "__main__":
    main()
