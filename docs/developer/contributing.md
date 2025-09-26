# 🤝 Contributing Guide

This guide explains how to contribute to the URL Shortener project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)

## 📜 Code of Conduct

This project follows a code of conduct to ensure a professional environment for all contributors. Be respectful and constructive in all interactions.

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub and clone your fork
git clone https://github.com/osmanmakhtoom/url-shortener.git
cd url-shortener

# Add upstream remote
git remote add upstream https://github.com/osmanmakhtoom/url-shortener.git
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start external services
docker compose up -d postgres redis rabbitmq

# Run database migrations
task db-migrate
```

### 3. Verify Setup

```bash
# Run tests to ensure everything works
task test

# Check code quality
task quality

# Start development server
task dev
```

## 🔄 Development Workflow

### 1. Create a Branch

```bash
# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

### 2. Make Changes

- Write your code following the [Code Standards](#code-standards)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
task test

# Run specific test categories
task test-services
task test-integration
task test-validation

# Check code quality
task quality

# Run security scan
task security-scan
```

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new feature description"
# or
git commit -m "fix: fix issue description"
```

### 5. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a pull request on GitHub
```

## 📏 Code Standards

### Python Code Style

- **Formatting**: Use Black for code formatting
- **Linting**: Use Ruff for linting
- **Import Sorting**: Use isort for import organization
- **Type Hints**: Use mypy for type checking

```bash
# Auto-format code
task format

# Run linting
task lint

# Sort imports
task lint-isort-fix

# Check types
task typecheck
```

### Code Quality Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have type hints
- [ ] Docstrings are present for public functions/classes
- [ ] No unused imports or variables
- [ ] All tests pass
- [ ] Code coverage is maintained
- [ ] Security scan passes

### Commit Message Format

Use conventional commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add rate limiting to shorten endpoint
fix(db): resolve connection pool exhaustion
docs(readme): update installation instructions
test(services): add comprehensive URL service tests
```

## 🧪 Testing

### Test Requirements

- **Coverage**: Maintain or improve test coverage
- **Quality**: All tests must pass
- **Categories**: Tests should be properly categorized
- **Documentation**: Test functions should be well-documented

### Running Tests

```bash
# Run all tests
task test

# Run with coverage
task test-coverage

# Run specific categories
task test-services         # Service layer tests
task test-integration      # Integration tests
task test-validation       # Schema validation tests
task test-business-logic   # Business logic tests

# Run in parallel (faster)
task test-parallel
```

### Writing Tests

```python
# Example test structure
import pytest
from app.services.url_service import URLService

class TestURLService:
    """Test cases for URLService."""
    
    async def test_create_short_url_success(self, db_session):
        """Test successful URL shortening."""
        service = URLService(db_session)
        result = await service.create_short("https://example.com")
        
        assert result is not None
        assert result.original_url == "https://example.com"
        assert len(result.short_code) == 6
```

## 📚 Documentation

### Documentation Requirements

- **API Documentation**: Update API docs for new endpoints
- **User Documentation**: Update user guides for new features
- **Developer Documentation**: Update development guides
- **Code Documentation**: Add docstrings to new functions/classes

### Documentation Structure

```
docs/
├── user/           # User-facing documentation
├── developer/      # Developer documentation
├── api/           # API documentation
├── deployment/    # Deployment guides
├── testing/       # Testing documentation
└── architecture/  # Architecture documentation
```

## 📤 Submitting Changes

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Update** documentation
6. **Submit** a pull request

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Coverage maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and quality checks
2. **Code Review**: Maintainers review the code
3. **Feedback**: Address any feedback or requested changes
4. **Approval**: Once approved, changes are merged

## 🐛 Issue Guidelines

### Reporting Bugs

When reporting bugs, include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, dependencies
- **Screenshots**: If applicable

### Feature Requests

When requesting features, include:

- **Description**: Clear description of the feature
- **Use Case**: Why this feature is needed
- **Proposed Solution**: How you think it should work
- **Alternatives**: Other solutions considered

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 🏷️ Labels and Milestones

### Labels

- **Priority**: `priority: high`, `priority: medium`, `priority: low`
- **Type**: `type: bug`, `type: feature`, `type: documentation`
- **Status**: `status: needs review`, `status: in progress`, `status: blocked`
- **Component**: `component: api`, `component: database`, `component: frontend`

### Milestones

- **Version Releases**: `v1.1.0`, `v1.2.0`
- **Sprints**: `Sprint 1`, `Sprint 2`
- **Epics**: `Performance Improvements`, `Security Enhancements`

## 🎯 Development Priorities

### High Priority
- Security vulnerabilities
- Critical bugs
- Performance issues
- Documentation gaps

### Medium Priority
- New features
- Code improvements
- Test coverage
- Developer experience

### Low Priority
- Nice-to-have features
- Code style improvements
- Minor optimizations

## 🆘 Getting Help

### Resources

- **Documentation**: [Complete Documentation](../README.md)
- **Issues**: [GitHub Issues](https://github.com/osmanmakhtoom/url-shortener/issues)
- **Discussions**: [GitHub Discussions](https://github.com/osmanmakhtoom/url-shortener/discussions)
- **Telegram**: [@osman_makhtoom](https://t.me/osman_makhtoom)

### Contact

- **Maintainer**: osmanmakhtoom@gmail.com
- **Community**: [@osman_makhtoom](https://t.me/osman_makhtoom)
- **LinkedIn**: [osman-makhtoom](https://linkedin.com/in/osman-makhtoom)
- **Security**: osmanmakhtoom@gmail.com

## 🏆 Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Mentioned in release notes
- **GitHub**: Listed as contributors
- **Documentation**: Credited in relevant sections

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Contributions are appreciated!** 🚀

Your contributions help make this project better for everyone. We appreciate your time and effort!
