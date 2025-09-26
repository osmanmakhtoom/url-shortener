# 🚀 URL Shortener

A high-performance, production-ready URL shortener service built with FastAPI, featuring comprehensive testing, security scanning, and enterprise-grade development tools.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.117+-green.svg)](https://fastapi.tiangolo.com)
[![Type Safety](https://img.shields.io/badge/Type%20Safety-100%25-brightgreen.svg)](#)
[![Test Coverage](coverage.svg)](#)
[![Production Ready](https://img.shields.io/badge/Production-Ready-success.svg)](#)

## ✨ Features

- 🔗 **URL Shortening**: Create short URLs with custom or auto-generated codes
- 📊 **Analytics**: Track visit counts and detailed statistics
- ⚡ **High Performance**: Sub-millisecond redirects with Redis caching
- 🛡️ **Security**: Comprehensive security scanning and validation
- 🧪 **Testing**: 126+ tests with 100% type safety
- 🐳 **Docker Ready**: Complete containerization with Docker Compose
- 📈 **Scalable**: Designed for horizontal scaling
- 🔧 **Developer Tools**: 120+ automation tasks for development

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/osmanmakhtoom/url-shortener.git
cd url-shortener

# Start all services
docker compose up -d

# The service will be available at http://localhost:8000
```

### API Usage

```bash
# Create a short URL
curl -X POST "http://localhost:8000/api/v1/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/very/long/url"}'

# Response
{
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url",
  "short_url": "/abc123",
  "created_at": "2025-01-26T10:30:00Z"
}

# Access the short URL
curl -L "http://localhost:8000/abc123"  # Redirects to original URL

# Get statistics
curl "http://localhost:8000/api/v1/stats/abc123"
```

## 📚 Documentation

📖 **Complete documentation is available in the [`docs/`](docs/) directory:**

- **[📖 Documentation Index](docs/README.md)** - Complete documentation overview
- **[👥 User Guide](docs/user/README.md)** - Project overview and user documentation
- **[🔧 Developer Tools](docs/developer/TASKFILE.md)** - 120+ automation tasks
- **[🚀 Deployment Guide](docs/deployment/DEPLOYMENT.md)** - Production deployment
- **[🔌 API Reference](docs/api/API.md)** - Complete API documentation
- **[🧪 Testing Guide](docs/testing/TESTING.md)** - Testing strategy and coverage
- **[🏗️ Architecture](docs/architecture/SCALABILITY.md)** - System architecture and design

## 🛠️ Development Toolbox

The project includes a comprehensive development toolbox with **120+ automation tasks**:

```bash
# Show all available tasks
task help

# Quick development workflow
task workflow-dev

# Complete testing workflow
task quick-test

# Production deployment
task workflow-deploy
```

**Key Task Categories:**
- 🐳 **Docker & Infrastructure** (20 tasks)
- 🗄️ **Database Operations** (15 tasks)
- 🧪 **Testing & Quality** (20 tasks)
- 🚀 **Development Workflow** (10 tasks)
- 🔧 **API & Service Management** (10 tasks)
- 🛠️ **Utilities & Helpers** (15 tasks)

## 🏗️ Architecture

- **Backend**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLModel ORM
- **Cache**: Redis for high-performance caching
- **Queue**: RabbitMQ for asynchronous processing
- **Monitoring**: Comprehensive logging and metrics
- **Security**: Multiple security scanning tools

## 📊 Project Status

- ✅ **100% Type Safety**: Complete mypy validation across all 49 source files
- ✅ **Comprehensive Testing**: 126+ tests covering all functionality and business logic
- ✅ **Zero Linting Issues**: Clean code with proper import organization
- ✅ **Production Ready**: Optimized and ready for deployment
- ✅ **Enterprise Tools**: 88 packages, 120+ automation tasks

## 🚀 Performance

- **Sub-millisecond redirects** with Redis caching
- **Horizontal scaling** support
- **Async processing** for analytics
- **Optimized database queries**
- **Comprehensive monitoring**

## 🛡️ Security

- **Comprehensive security scanning** (Bandit, Safety, pip-audit)
- **Input validation** and sanitization
- **Rate limiting** and abuse prevention
- **Secure configuration** management
- **Regular dependency updates**

## 📈 Monitoring

- **Health checks** and status endpoints
- **Comprehensive logging** with structured output
- **Performance metrics** and monitoring
- **Error tracking** and alerting
- **Resource usage** monitoring

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/developer/contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 📧 **Email**: osmanmakhtoom@gmail.com
- 💬 **Telegram**: [@osman_makhtoom](https://t.me/osman_makhtoom)
- 🔗 **LinkedIn**: [osman-makhtoom](https://linkedin.com/in/osman-makhtoom)
- 🐛 **Issues**: [GitHub Issues](https://github.com/osmanmakhtoom/url-shortener/issues)
- 📖 **Documentation**: [Complete Documentation](docs/README.md)

---

**Built with ❤️ using FastAPI, SQLModel, Redis, and RabbitMQ**
