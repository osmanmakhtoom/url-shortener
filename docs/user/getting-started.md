# 🚀 Getting Started Guide

This guide will help you get the URL Shortener service up and running quickly.

## 📋 Prerequisites

- **Docker** and **Docker Compose** (recommended)
- **Python 3.12+** (for local development)
- **Git** (for cloning the repository)

## 🐳 Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/osmanmakhtoom/url-shortener.git
cd url-shortener
```

### 2. Start the Services

```bash
# Start all services (backend, database, Redis, RabbitMQ)
docker compose up -d

# Check service status
docker compose ps
```

### 3. Verify Installation

```bash
# Check if the service is running
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "database": "connected",
  "redis": "connected"
}
```

### 4. Access the Service

- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🐍 Local Development Setup

### 1. Clone and Setup

```bash
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
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

### 4. Initialize Database

```bash
# Run database migrations
alembic upgrade head

# Or use the task
task db-migrate
```

### 5. Start the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Using the Development Toolbox

The project includes 120+ automation tasks for development:

```bash
# Show all available tasks
task help

# Quick development workflow
task workflow-dev

# Run tests
task test

# Check code quality
task quality

# Run security scan
task security-scan
```

## 📖 Getting Started

### 1. Create a Short URL

```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/very/long/url"}'
```

### 2. Access the Short URL

```bash
# Use the short_code from the response
curl -L "http://localhost:8000/abc123"
```

### 3. Check Statistics

```bash
curl "http://localhost:8000/api/v1/stats/abc123"
```

## 🎯 Additional Features

1. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Read the User Guide**: Check out the [User Guide](user-guide.md) for detailed usage instructions
3. **Development**: See the [Developer Documentation](../developer/development-setup.md) for development setup
4. **Deployment**: Follow the [Deployment Guide](../deployment/DEPLOYMENT.md) for production deployment

## 🆘 Troubleshooting

### Common Issues

#### Service Not Starting
```bash
# Check service logs
docker compose logs backend

# Restart services
docker compose restart
```

#### Database Connection Issues
```bash
# Check database status
docker compose exec postgres pg_isready

# Reset database
docker compose down -v
docker compose up -d
```

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Getting Help

- 📖 **Documentation**: [Complete Documentation](../README.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/osmanmakhtoom/url-shortener/issues)
- 💬 **Telegram**: [@osman_makhtoom](https://t.me/osman_makhtoom)
- 📧 **Email**: osmanmakhtoom@gmail.com

## 🎉 Success!

The URL Shortener service is now ready for use! 

- ✅ Service is running
- ✅ API is accessible
- ✅ Database is connected
- ✅ Ready for development or production use

**Happy URL shortening!** 🚀
