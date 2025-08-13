# Number Trainer - Project Memory

## Project Overview

Number Trainer is a comprehensive Python application for practicing mental arithmetic with multiple interfaces (GUI, CLI, Web). The project features a modular architecture with clean separation of concerns and comprehensive testing.

## Architecture

### Modular Structure
```
number_trainer/
├── src/number_trainer/          # Main package
│   ├── core/                    # Business logic
│   │   ├── models.py           # Exercise, Result, Operation
│   │   └── trainer.py          # MathTrainer class
│   ├── gui/                    # Graphical interface
│   │   ├── app.py             # NumberTrainerApp
│   │   └── styles.py          # GUI styles
│   ├── cli/                   # Console interface
│   │   └── console.py         # run_console_trainer
│   └── web/                   # Web interface (FastAPI)
│       ├── main.py           # FastAPI application
│       ├── routes.py         # API endpoints
│       ├── models.py         # Pydantic models
│       └── static/           # HTML/CSS/JS assets
├── tests/                     # All tests
│   ├── test_core/            # Business logic tests
│   ├── test_gui/             # GUI tests
│   └── test_web/             # Web API tests
├── main.py                   # GUI entry point
├── web_main.py              # Web entry point
└── demo.py                  # Console demo
```

## Interfaces

### 1. GUI Interface (Tkinter)
- **Design**: Modern, minimalist interface with card-based layout
- **Color Scheme**: #2563eb (blue), #10b981 (green), #f8fafc (background)
- **Typography**: SF Pro Display font for modern appearance
- **Features**:
  - Welcome screen with difficulty selection (1, 1-2, 2-3 digits)
  - Interactive exercises with input field
  - Real-time timing of exercise completion
  - Statistics panel (total/correct/incorrect/accuracy)
  - Results feedback with auto-progression
- **Hotkeys**:
  - Enter (check answer)
  - Escape (main screen)
  - Ctrl+N (new exercise)
- **Window**: Centered 900x700 pixels with auto-focus on input

### 2. CLI Interface (Console)
- Simple console-based interface for terminal users
- Direct integration with core MathTrainer business logic
- Minimal dependencies for lightweight usage

### 3. Web Interface (FastAPI)
- **Framework**: FastAPI with async support
- **Design**: Responsive HTML/CSS/JS matching GUI style
- **Features**:
  - Adaptive design for desktop and mobile
  - Modern interface with same color scheme as GUI
  - Hotkeys: Enter (check), Escape (main menu)
  - Auto-progression after correct answers
- **API Endpoints**:
  - `GET /` - Main page
  - `POST /api/exercise/new` - Create exercise
  - `POST /api/exercise/check` - Check answer
  - `GET /api/stats` - Get statistics
  - `GET /api/health` - Health check
- **Server**: Runs on http://localhost:8000

## Core Business Logic

### MathTrainer Class
- Separate trainers for each difficulty level (1, 2, 3 digits)
- Integration across all interfaces (GUI, CLI, Web)
- Exercise generation and answer validation
- Statistics tracking and persistence

### Models
- **Exercise**: Mathematical problem representation
- **Result**: Answer result with timing information
- **Operation**: Mathematical operations (addition, subtraction, etc.)

## Development Tools & Automation

### Taskfile.yml (20+ Commands)
- **Installation**: `task install`, `task install-dev`, `task dev`
- **Running**:
  - `task run` (GUI)
  - `task run-console` (CLI)
  - `task run-web` (Web server)
  - `task demo` (Console demo)
- **Testing**: `task test`, `task test-cov`, `task test-watch`
- **Code Quality**: `task lint`, `task format`, `task ci`
- **Utilities**: `task clean`, `task health`, `task info`, `task help`

### Package Management
- **Tool**: uv (modern Python package manager)
- **Python Version**: 3.8+
- **Dependencies**: Managed via pyproject.toml

### Code Quality
- **Type Checking**: mypy (all 19 source files pass with 0 errors)
- **Formatting**: black, isort
- **Linting**: flake8
- **Testing**: pytest with coverage reporting

## Testing

### Test Coverage
- **Total Tests**: 38 tests across all modules
- **Test Structure**:
  - `test_core/` - Business logic tests
  - `test_gui/` - GUI component tests
  - `test_web/` - Web API tests (14 tests)
- **Status**: All tests pass successfully

## Type Safety

### MyPy Compliance
Successfully resolved all 17 mypy type checking issues:

- **GUI App**: Added type annotations for parameters, dynamic attributes, lambda functions
- **Console CLI**: Fixed check_answer method calls with proper parameter passing
- **Web Routes**: Added return type annotations for async functions, fixed integer casting
- **Web Main**: Added proper return type annotations

Result: 0 mypy errors across all 19 source files.

## Key Features

### Exercise Management
- Multiple difficulty levels (1-digit, 1-2 digit, 2-3 digit numbers)
- Real-time exercise timing
- Answer validation with immediate feedback
- Statistics tracking (accuracy, total attempts, etc.)

### User Experience
- Consistent design language across all interfaces
- Keyboard shortcuts for efficient navigation
- Auto-focus and auto-progression features
- Error handling and input validation
- Mobile-responsive web interface

### Technical Excellence
- Clean modular architecture
- Comprehensive test coverage
- Full type safety with mypy
- Modern development tooling
- CI/CD automation with Taskfile

## Quick Start

```bash
# Install dependencies
task install-dev

# Run GUI version
task run

# Run console version
task run-console

# Run web version
task run-web

# Run all tests
task test

# Check code quality
task ci
```

## Project Status

- ✅ All 38 tests passing
- ✅ 0 mypy type errors
- ✅ Three fully functional interfaces (GUI, CLI, Web)
- ✅ Comprehensive automation and tooling
- ✅ Modern, maintainable codebase
- ✅ Full documentation and project memory

---

*Last Updated: 2025-08-08*
*Project Location: `/Users/eravniushkin/workspace/personal/number_trainer`*
