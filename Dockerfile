# Ultra-lightweight Alpine-based build
FROM python:3.13-alpine AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    && pip install --no-cache-dir uv

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies in virtual environment
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-alpine AS production

# Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000
ENV HOST=0.0.0.0
ENV WORKERS=1
ENV LOG_LEVEL=info
ENV PATH="/app/.venv/bin:$PATH"

# Install only runtime dependencies
RUN apk add --no-cache curl \
    && addgroup -g 1000 appuser \
    && adduser -D -u 1000 -G appuser appuser

# Set work directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code with correct ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
CMD ["python", "-m", "src.number_trainer.web.production"]
