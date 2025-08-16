# Claude Memory

## Git Commit Guidelines
- Do NOT add "🤖 Generated with [Claude Code]" signatures
- Do NOT add "Co-Authored-By: Claude <noreply@anthropic.com>"
- Use only user's git credentials for commit authorship
- Keep commit messages clean without Claude Code references
- Same applies to PR/MR descriptions

## Rules
- All documentation put into docs dir

## Project Overview
Number Trainer is a mathematical exercise application designed to help users practice basic arithmetic (addition/subtraction) with different difficulty levels. The project demonstrates modern Python development practices with multiple interfaces and comprehensive testing.

### Application Interfaces
1. **GUI Interface** (Tkinter)
   - Modern minimalist design with animations
   - Difficulty selection (1-3 digits)
   - Real-time statistics tracking
   - Located in `src/number_trainer/gui/`

2. **Console Interface** (CLI)
   - Command-line interactive trainer
   - Simple text-based interface
   - Located in `src/number_trainer/cli/`

3. **Web Interface** (FastAPI)
   - REST API with HTML frontend
   - HTTP endpoints for exercise management
   - Health checks and statistics
   - Located in `src/number_trainer/web/`

### Core Architecture
- **Core Logic** (`src/number_trainer/core/`):
  - `trainer.py`: Main MathTrainer class
  - `models.py`: Data models (Exercise, Result, Operation)
  - Pure business logic, UI-independent

### Technology Stack
- **Python 3.13** (recently migrated from 3.8.1+)
- **FastAPI** for web interface
- **Uvicorn** for ASGI server
- **Pydantic** for data validation
- **Tkinter** for GUI (built-in)
- **pytest** for testing with coverage
- **Ruff** for linting and formatting
- **MyPy** for type checking
- **uv** for fast dependency management

### Development Workflow
- **Task-based commands** via `Taskfile.yml`:
  - `task test` - Unit tests only
  - `task test-integration` - Docker integration tests
  - `task test-all` - All tests with coverage
  - `task lint` - Code quality checks
  - `task format` - Code formatting
  - `task ci` - Full CI pipeline
- **Pre-commit hooks** for code quality
- **Conventional commits** with semantic versioning

### Testing Strategy
- **Unit Tests**: Core logic and web API
- **Integration Tests**: Docker container end-to-end testing
- **pytest markers**: `integration` for Docker tests
- **Coverage reporting**: HTML reports generated
- **CI/CD**: GitHub Actions with comprehensive checks

### Docker & Deployment
- **Ultra-optimized Alpine images**: 170MB (79% size reduction achieved)
- **Multi-stage builds** for production efficiency
- **Health checks** and proper signal handling
- **Security**: Non-root user, minimal attack surface
- **Docker variants**:
  - Main: `python:3.13-alpine` (current)
  - Backup: `Dockerfile.slim` (multi-stage Debian)
  - Original: `Dockerfile.original` (single-stage)

### CI/CD Pipeline
- **GitHub Actions workflows**:
  - `ci.yml`: Testing and code quality
  - `docker-publish.yml`: Build and publish images
- **Integration tests** run in CI before publishing
- **Automatic versioning** from pyproject.toml
- **Multi-platform support** (ARM64/AMD64)

### Code Quality Standards
- **Type hints**: Full typing with mypy compliance
- **Modern Python**: Using Python 3.13 features
- **Linting**: Ruff with strict rules
- **Formatting**: Consistent code style
- **Documentation**: Comprehensive docstrings

### Project Structure
```
src/number_trainer/
├── core/           # Business logic
├── gui/            # Tkinter interface
├── cli/            # Console interface
└── web/            # FastAPI web app
tests/
├── test_core/      # Unit tests
├── test_web/       # API tests
└── integration/    # Docker integration tests
```

### Key Features
- **Difficulty Levels**: 1-3 digit numbers
- **Operations**: Addition and subtraction
- **Statistics Tracking**: Accuracy, speed, counts
- **Exercise Generation**: Random with constraints
- **Answer Validation**: Immediate feedback
- **Session Management**: Persistent training sessions

### Development Practices
- **Dependency isolation**: Virtual environments with uv
- **Lock files**: Reproducible builds with uv.lock
- **Security**: Dependency scanning and updates
- **Performance**: Optimized Docker images and fast tests
- **Maintainability**: Modular architecture and comprehensive tests

### Recent Achievements
1. **Python 3.13 Migration**: Full upgrade with performance benefits
2. **Docker Optimization**: 79% size reduction (801MB → 170MB)
3. **Integration Testing**: Comprehensive Docker test suite
4. **CI/CD Enhancement**: Reliable automated pipelines
5. **Code Modernization**: Updated to latest Python syntax

### Monitoring & Health
- **Health endpoints**: `/api/health` for monitoring
- **Docker health checks**: Container lifecycle management
- **Error handling**: Graceful degradation and recovery
- **Logging**: Structured logging for debugging

This project serves as an excellent example of modern Python development with multiple interfaces, comprehensive testing, and production-ready deployment practices.
