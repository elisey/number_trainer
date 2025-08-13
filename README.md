# Number Trainer


Mathematical trainer for learning arithmetic with support for GUI, console, and web interfaces.

## Project Structure

```
number_trainer/
├── src/
│   └── number_trainer/          # Main package
│       ├── core/                # Business logic
│       │   ├── models.py        # Data models
│       │   └── trainer.py       # Main trainer class
│       ├── gui/                 # Graphical interface
│       │   ├── app.py          # GUI application
│       │   └── styles.py       # Styling
│       ├── cli/                 # Console interface
│       │   └── console.py       # Console version
│       └── web/                 # Web interface
│           ├── app.py          # FastAPI application
│           ├── routes.py       # API routes
│           ├── models.py       # Pydantic models
│           ├── main.py         # Web server entry point
│           └── static/         # Static files (CSS, JS)
├── tests/                       # Tests
│   ├── test_core/              # Business logic tests
│   ├── test_gui/               # GUI tests
│   └── test_web/               # Web interface tests
├── main.py                      # GUI entry point
├── demo.py                      # Console demo
└── pyproject.toml              # Project configuration
```

## Installation and Setup

The project uses `uv` for dependency management.

### Requirements
- Python >= 3.8
- uv

### Quick Start with Taskfile
```bash
# Show all available commands
task --list

# Setup development environment
task dev

# Launch GUI application
task run

# Launch console version
task run-console

# Run tests
task test
```

### Main Commands
```bash
# 📦 INSTALLATION
task install         # Install dependencies
task install-dev     # Install dev dependencies

# 🏃 LAUNCH
task run             # Launch GUI application
task run-console     # Launch console version
task run-web         # Launch web server (browser version)
task demo            # Show demonstration

# 🧪 TESTING
task test            # Run tests
task test-cov        # Tests with code coverage
task test-watch      # Tests in watch mode

# 🔧 CODE QUALITY
task lint            # Check with linters
task format          # Format code
task ci              # All CI checks
task pre-commit      # Run pre-commit on all files

# ℹ️ INFORMATION
task info            # Project information
task health          # Health check
task help            # Detailed help
```

### Alternative Launch
```bash
# GUI version
uv run python3 main.py
uv run number-trainer

# Console version
uv run python3 demo.py
uv run number-trainer-console

# Web version
uv run python3 web_main.py
uv run number-trainer-web
```

## Pre-commit Hooks

The project is configured with pre-commit hooks for automatic code quality checks on each commit.

### Pre-commit Setup

```bash
task install-dev
task install-hooks
```

### What is Checked Automatically

On each commit, the following runs:
- **task ci** - all code quality checks (formatting, linting, tests)
- **pre-commit hooks** - additional checks:
  - Remove trailing whitespace
  - Fix file endings
  - Check YAML/JSON files
  - Check for merge conflicts
  - Check for filename case conflicts
  - Check docstrings at file beginning
  - Check for debug statements

### Manual Check Execution

```bash
# Run pre-commit on all files
task pre-commit

# Run only task ci
task ci

# Run individual checks
task format-check
task lint
task test
```

## Web Interface

The web version of Number Trainer provides a modern browser interface with responsive design for desktop and mobile devices.

### Launch Web Server
```bash
task run-web
# or
uv run python3 web_main.py
```

After launching, open your browser and go to: http://localhost:8000

### Web Interface Features
- **Responsive Design** - works on desktop and mobile devices
- **Modern UI** - uses color scheme from GUI version
- **REST API** - full API for integration
- **Hotkeys** - Enter (check), Escape (main menu)
- **Real-time Statistics** - progress tracking
- **Auto-advance** - automatic transition to next exercise

### API Endpoints
- `GET /` - main application page
- `POST /api/exercise/new` - create new exercise
- `POST /api/exercise/check` - check answer
- `GET /api/stats` - get statistics
- `GET /api/health` - server health check

## Docker

Number Trainer supports running in Docker containers for simplified deployment and environment isolation.

### Quick Start with Docker

```bash
# Build and run with Docker Compose
task docker-compose-up

# Or build and run manually
task docker-build
task docker-run
```

### Docker Commands

```bash
# 🐳 DOCKER
task docker-build           # Build Docker image
task docker-run             # Run Docker container
task docker-stop            # Stop containers
task docker-clean           # Clean images and containers

# 🐳 DOCKER COMPOSE
task docker-compose-up      # Launch via Docker Compose (development)
task docker-compose-down    # Stop Docker Compose
task docker-compose-logs    # Show logs
task docker-compose-build   # Rebuild image

# 🐳 PRODUCTION DOCKER
task docker-compose-prod    # Launch in production mode
task docker-compose-prod-down # Stop production
task docker-compose-prod-logs # Production logs
task docker-compose-prod-build # Rebuild production image

# 🐳 GITHUB CONTAINER REGISTRY
task docker-build-ghcr      # Build for GitHub Container Registry
task docker-push-ghcr       # Publish to GHCR
task docker-publish         # Build and publish
```

### Running from GitHub Container Registry

```bash
# Run latest version
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:latest

# Run specific version
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:v1.0.0

# Run major.minor version (latest patch)
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:1.0
```

## 🚀 Web Release Instructions

### **Release Workflow**

Number Trainer uses an automated release process through GitHub Actions. Docker images are published only when version tags are created.

#### **1. Release Preparation**

```bash
# Make sure you're on the main branch
git checkout main
git pull origin main

# Check current version in pyproject.toml
cat pyproject.toml | grep version
```

#### **2. Version Update**

```bash
# Edit pyproject.toml
# Change version = "0.1.0" to new version, e.g. "1.0.0"

# Commit version changes
git add pyproject.toml
git commit -m "Bump version to 1.0.0"
git push origin main
```

#### **3. Creating Release**

```bash
# Create release tag
git tag v1.0.0

# Push tag to GitHub
git push origin v1.0.0
```

#### **4. Automatic Build and Publication**

After pushing the tag, GitHub Actions automatically:
- ✅ Builds Docker image
- ✅ Tests its functionality
- ✅ Publishes to GitHub Container Registry
- ✅ Creates tags: `v1.0.0`, `1.0`, `latest`

#### **5. Release Verification**

```bash
# Check that image is available
docker pull ghcr.io/[username]/number-trainer:v1.0.0

# Test locally
docker run -p 8000:8000 ghcr.io/[username]/number-trainer:v1.0.0
```

### **Versioning Strategy**

#### **Semantic Versioning (SemVer)**
- `v1.0.0` - Major.Minor.Patch
- `v1.1.0` - New features (minor)
- `v2.0.0` - Breaking changes (major)

#### **Available Tags**
- `latest` - Latest stable release
- `v1.0.0` - Specific version
- `1.0` - Latest patch for major.minor

### **Development vs Production**

#### **Development Workflow**
```bash
# Regular development
git push origin main
# → Triggers test build (no publication)
```

#### **Production Release**
```bash
# Release
git tag v1.0.0 && git push origin v1.0.0
# → Triggers production build and publication
```

### **Deployment Examples**

#### **Local Development**
```bash
# Launch local version
task docker-compose-up
```

#### **Production Deployment**
```bash
# Launch production version
docker run -d -p 8000:8000 \
  --name number-trainer \
  ghcr.io/[username]/number-trainer:v1.0.0
```

#### **Docker Compose Production**
```bash
# Create docker-compose.yml
version: '3.8'
services:
  number-trainer:
    image: ghcr.io/[username]/number-trainer:v1.0.0
    ports:
      - "8000:8000"
    restart: unless-stopped

# Launch
docker-compose up -d
```

### **Rollback Strategy**

```bash
# Rollback to previous version
docker stop number-trainer
docker run -d -p 8000:8000 \
  --name number-trainer \
  ghcr.io/[username]/number-trainer:v0.9.0
```

### **Monitoring Releases**

- **GitHub Actions**: Check build status in Actions tab
- **Container Registry**: View published images in Packages
- **Health Check**: `curl http://localhost:8000/api/health`

### **Quick Reference**

#### **Common Release Commands**
```bash
# Create new release
git tag v1.0.0 && git push origin v1.0.0

# List all tags
git tag -l

# Delete local tag (if needed)
git tag -d v1.0.0

# Delete remote tag (if needed)
git push origin --delete v1.0.0
```

#### **Check Release Status**
```bash
# Check available images
docker search ghcr.io/[username]/number-trainer

# Check image tags
docker pull ghcr.io/[username]/number-trainer:latest
docker images | grep number-trainer
```

### Environment Variables

- `PORT` - port for application launch (default: 8000)
- `HOST` - host for binding (default: 0.0.0.0)
- `WORKERS` - number of worker processes (default: 1, production: 4)
- `LOG_LEVEL` - logging level (default: info, production: warning)
- `PYTHONUNBUFFERED` - disable Python buffering (default: 1)

### Production vs Development

**Development mode:**
- Auto-reload on code changes
- Detailed logging
- 1 worker process

**Production mode:**
- Auto-reload disabled
- Optimized logging
- 4 worker processes
- Resource limits (CPU/Memory)
- Additional security measures
- Read-only file system (except temporary directories)

### Health Check

The container includes a health check that verifies API availability:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status": "healthy", "service": "number-trainer-web"}
```

## Project Structure

- `main.py` - main application file with tkinter GUI
- `pyproject.toml` - project configuration
- `README.md` - documentation

## Development

The application is built using:
- **Python** - main programming language
- **tkinter** - built-in GUI library for desktop version
- **FastAPI** - modern web framework for API
- **uvicorn** - ASGI server for web application
- **HTML/CSS/JavaScript** - web interface frontend
- **uv** - dependency and project management

### Architecture
- **Modular structure** - separation into core, gui, cli, web
- **Unified business logic** - all interfaces use common `MathTrainer`
- **REST API** - standardized interaction with web interface
- **Responsive design** - support for desktop and mobile devices
