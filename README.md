# Number Trainer

Mathematical trainer for practice arithmetic with support for GUI, console, and web interfaces.

## Features

- **Multiple Interfaces**: GUI (tkinter), Console, and Web (FastAPI)
- **Difficulty Levels**: Customizable difficulty settings
- **Progress Tracking**: Statistics and performance monitoring
- **Web API**: REST API for integration
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Requirements
- Python >= 3.8
- [uv](https://github.com/astral-sh/uv)

### Installation
```bash
# Install dependencies
task install

# Install pre-commit hooks (optional)
task install-hooks
```

### Running the Application
```bash
# GUI version (desktop)
task run

# Console version
task run-console

# Web version (browser)
task run-web
# Then open http://localhost:8000
```

## Development

### Available Commands
```bash
# Installation
task install          # Install all dependencies

# Running
task run              # Launch GUI application
task run-console      # Launch console version
task run-web          # Launch web server

# Testing & Quality
task test             # Run tests with coverage
task lint             # Check code with linters
task format           # Format code
task ci               # Run all CI checks

# Cleanup
task clean            # Clean temporary files
```

### Project Structure
```
src/number_trainer/
├── core/             # Business logic
├── gui/              # Desktop interface (tkinter)
├── cli/              # Console interface
└── web/              # Web interface (FastAPI)
    ├── static/       # CSS, JS files
    └── templates/    # HTML templates
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Install development dependencies**: `task install`
4. **Set up pre-commit hooks**: `task install-hooks`
5. **Make your changes**
6. **Run tests and checks**: `task ci`
7. **Commit your changes**: `git commit -m "feat: your feature"`
8. **Push to your branch**: `git push origin feature/your-feature`
9. **Create a Pull Request**

### Code Quality

This project uses automated code quality checks:
- **Formatting**: `ruff format`
- **Linting**: `ruff check` + `mypy`
- **Testing**: `pytest` with coverage
- **Pre-commit hooks**: Run automatically on commits

All checks must pass before merging. Run `task ci` to verify locally.

## Deploying Web Version

### Local Development
```bash
# Start development server
task run-web

# Access at http://localhost:8000
```

### Production Deployment

#### Option 1: Direct Python
```bash
# Install dependencies
uv sync --all-groups

# Run production server
uv run uvicorn src.number_trainer.web.app:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Option 2: Docker
```bash
# Build image
docker build -t number-trainer .

# Run container
docker run -p 8000:8000 number-trainer
```

#### Option 3: Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  number-trainer:
    build: .
    ports:
      - "8000:8000"
    environment:
      - WORKERS=4
      - LOG_LEVEL=warning
    restart: unless-stopped
```

```bash
docker-compose up -d
```

### Environment Variables
- `PORT` - Server port (default: 8000)
- `HOST` - Bind address (default: 0.0.0.0)
- `WORKERS` - Number of worker processes (default: 1)
- `LOG_LEVEL` - Logging level (default: info)

### API Endpoints
- `GET /` - Web application
- `POST /api/exercise/new` - Generate new exercise
- `POST /api/exercise/check` - Check answer
- `GET /api/stats` - Get statistics
- `GET /api/health` - Health check

### Health Check
```bash
curl http://localhost:8000/api/health
# Expected: {"status": "healthy", "service": "number-trainer-web"}
```

## License

This project is available under the MIT License.
