# 🔧 Development Setup Guide

This guide will help you set up a complete development environment for the URL Shortener project.

## 📋 Prerequisites

- **Python 3.12+**
- **Docker** and **Docker Compose**
- **Git**
- **VS Code** (recommended) or your preferred IDE

## 🚀 Quick Setup

### 1. Clone and Initialize

```bash
# Clone the repository
git clone https://github.com/osmanmakhtoom/url-shortener.git
cd url-shortener

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start External Services

```bash
# Start database, Redis, and RabbitMQ
docker compose up -d postgres redis rabbitmq

# Verify services are running
docker compose ps
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

### 4. Initialize Database

```bash
# Run migrations
task db-migrate

# Or manually
alembic upgrade head
```

### 5. Start Development Server

```bash
# Start with auto-reload
task dev

# Or manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🛠️ Development Toolbox

The project includes **120+ automation tasks** for development:

### Core Development Tasks

```bash
# Development workflow
task workflow-dev          # Complete development workflow
task dev                   # Start development server
task dev-clean             # Clean development environment
task dev-status            # Check development status
```

### Testing Tasks

```bash
# Testing
task test                  # Run all tests
task test-parallel         # Run tests in parallel
task test-coverage         # Run with coverage
task test-html-report      # Generate HTML test report
task test-benchmark        # Run performance benchmarks
```

### Code Quality Tasks

```bash
# Code quality
task quality               # Run all quality checks
task quality-fix           # Auto-fix quality issues
task lint                  # Run linting
task format                # Format code
task typecheck             # Run type checking
```

### Security Tasks

```bash
# Security
task security-scan         # Run comprehensive security scan
task security-bandit       # Run Bandit security scan
task security-safety       # Run Safety vulnerability scan
task security-pip-audit    # Run pip-audit dependency scan
```

### Database Tasks

```bash
# Database
task db-migrate            # Run database migrations
task db-reset              # Reset database
task db-backup             # Backup database
task db-restore            # Restore database
task shell-db              # Open database shell
```

### Docker Tasks

```bash
# Docker
task build                 # Build Docker images
task up                    # Start all services
task down                  # Stop all services
task logs                  # View service logs
task shell                 # Open shell in container
```

## 🔧 IDE Setup

### VS Code Configuration

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true,
    ".mypy_cache": true
  }
}
```

### VS Code Extensions

Recommended extensions:

- **Python** - Python language support
- **Pylance** - Fast Python language server
- **Black Formatter** - Code formatting
- **Ruff** - Fast Python linter
- **Python Test Explorer** - Test discovery and running
- **Docker** - Docker support
- **GitLens** - Git supercharged

## 🧪 Testing Setup

### Running Tests

```bash
# Run all tests
task test

# Run specific test categories
task test-services         # Service layer tests
task test-integration      # Integration tests
task test-validation       # Validation tests
task test-business-logic   # Business logic tests

# Run with coverage
task test-coverage

# Run in parallel (faster)
task test-parallel
```

### Test Structure

```
tests/
├── conftest.py                    # Pytest configuration
├── test_api_comprehensive.py      # API integration tests
├── test_business_logic_and_errors.py  # Business logic tests
├── test_services_comprehensive.py # Service layer tests
├── test_validation_and_schemas.py # Schema validation tests
└── test_runner.py                 # Test runner utilities
```

## 🔍 Code Quality

### Linting and Formatting

```bash
# Run all quality checks
task quality

# Auto-fix issues
task quality-fix

# Individual tools
task lint                  # Ruff linting
task lint-black           # Black formatting
task lint-isort           # Import sorting
task lint-flake8          # Flake8 linting
task format               # Format code
task typecheck            # MyPy type checking
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
task pre-commit-install

# Run pre-commit hooks
task pre-commit-run
```

## 🐳 Docker Development

### Development with Docker

```bash
# Start all services
task up

# Start only external services
docker compose up -d postgres redis rabbitmq

# View logs
task logs

# Open shell in container
task shell
```

### Docker Compose Services

- **backend**: FastAPI application
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **rabbitmq**: RabbitMQ message queue
- **nginx**: Reverse proxy (optional)

## 📊 Monitoring and Debugging

### Health Checks

```bash
# Check service health
curl http://localhost:8000/health

# Check database connection
task db-status

# Check Redis connection
task cache-info

# Check RabbitMQ connection
task queue-info
```

### Logging

```bash
# View application logs
task logs-backend

# View database logs
task logs-db

# View Redis logs
task logs-redis

# View RabbitMQ logs
task logs-rabbitmq
```

## 🚀 Performance Testing

### Load Testing

```bash
# Run load tests
task load-test

# Run stress tests
task stress-test

# Profile memory usage
task profile-memory

# Profile CPU usage
task profile-cpu
```

## 🔧 Troubleshooting

### Common Issues

#### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Database Issues
```bash
# Reset database
task db-reset

# Check database status
task db-status
```

#### Port Conflicts
```bash
# Check port usage
lsof -i :8000

# Change port in .env or docker-compose.yml
```

#### Dependency Issues
```bash
# Update dependencies
task update-deps

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Additional Resources

- **[TASKFILE.md](TASKFILE.md)** - Complete development toolbox documentation
- **[API Documentation](../api/API.md)** - API reference and examples
- **[Testing Guide](../testing/TESTING.md)** - Testing strategy and coverage
- **[Architecture Documentation](../architecture/SERVICE_ORIENTED_DESIGN.md)** - System architecture

## 🎯 Development Workflow

1. **Explore the Codebase**: Familiarize yourself with the project structure
2. **Run Tests**: Ensure all tests pass
3. **Check Code Quality**: Run quality checks and fix any issues
4. **Start Developing**: Begin contributing to the project
5. **Read Documentation**: Explore the complete documentation

## 🆘 Getting Help

- 📖 **Documentation**: [Complete Documentation](../README.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/osmanmakhtoom/url-shortener/issues)
- 💬 **Telegram**: [@osman_makhtoom](https://t.me/osman_makhtoom)
- 📧 **Email**: osmanmakhtoom@gmail.com

---

**Ready for development!** 🚀
