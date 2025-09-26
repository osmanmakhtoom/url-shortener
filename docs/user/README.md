# 🚀 URL Shortener Service

A high-performance, production-ready URL shortener service built with **FastAPI**, **PostgreSQL**, **Redis**, and **RabbitMQ**. Features service-oriented architecture, comprehensive testing, and enterprise-grade type safety.

## ✨ Features

- **⚡ High Performance**: Sub-millisecond redirects with Redis caching
- **🏗️ Service-Oriented Architecture**: Clean separation of concerns with composable services
- **🔒 Type Safety**: 100% type coverage with mypy validation
- **🧪 Comprehensive Testing**: 126+ tests covering functionality, integration, and business logic
- **📊 Analytics**: Real-time visit tracking with detailed analytics
- **🔄 Async Processing**: Non-blocking visit logging with RabbitMQ workers
- **🗃️ Soft Deletes**: Data preservation with soft delete functionality
- **📈 Scalable**: Horizontal scaling with independent service scaling
- **🐳 Docker Ready**: Complete containerization with docker-compose
- **📝 Well Documented**: Comprehensive documentation and examples

## 🏗️ Architecture

### Service-Oriented Design
```
BaseService
├── ModelService[T] (Generic CRUD with soft-delete awareness)
│   ├── URLService (URL-specific business logic)
│   └── VisitService (Visit-specific business logic)
├── SoftDeleteService[T] (Soft delete operations)
└── TimestampService[T] (Timestamp management)
```

### Technology Stack
- **Backend**: FastAPI (async Python)
- **Database**: PostgreSQL with SQLModel/asyncpg
- **Cache**: Redis with asyncio client
- **Queue**: RabbitMQ with aio-pika
- **Type Checking**: mypy with 100% coverage
- **Testing**: pytest with comprehensive test suites
- **Containerization**: Docker & docker-compose

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### 1. Clone and Setup
```bash
git clone git@github.com:osmanmakhtoom/url-shortener.git
cd url_shortener
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Start Services
```bash
# Start all services (PostgreSQL, Redis, RabbitMQ, API)
docker-compose up -d

# View logs
docker-compose logs -f backend
```

### 4. Initialize Database
```bash
# Run database migrations
docker-compose exec backend python -m alembic upgrade head

# Or create tables directly (development)
docker-compose exec backend python app/management.py create-tables
```

### 5. Verify Installation
```bash
# Check health
curl http://localhost:8000/health

# Test API
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### 1. Shorten URL
```bash
POST /api/v1/shorten
Content-Type: application/json

{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "short_code": "abc123",
  "original_url": "https://example.com",
  "short_url": "/abc123",
  "created_at": "2023-01-01T00:00:00"
}
```

#### 2. Redirect to Original URL
```bash
GET /{short_code}
```

**Response:** `307 Temporary Redirect` to original URL

#### 3. Get URL Statistics
```bash
GET /api/v1/stats/{short_code}
```

**Response:**
```json
{
  "original_url": "https://example.com",
  "short_code": "abc123",
  "visit_count": 42,
  "created_at": "2023-01-01T00:00:00"
}
```

#### 4. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T00:00:00",
  "version": "1.0.0",
  "environment": "development",
  "database": "healthy",
  "redis": "healthy",
  "rabbitmq": "healthy"
}
```

## 🧪 Testing

### Run All Tests
```bash
# Run comprehensive test suite
task test

# Run with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Run specific test categories
docker-compose exec backend pytest tests/test_services_comprehensive.py -v
docker-compose exec backend pytest tests/test_api_comprehensive.py -v
```

### Test Coverage
- **Overall Coverage**: 85%+
- **Service Layer**: 90%+
- **API Layer**: 95%+
- **Business Logic**: 95%+

### Test Categories
- **Functionality Tests**: Basic component functionality
- **Integration Tests**: Component integration and external systems
- **Response Type Tests**: HTTP status codes and response types
- **Response Data Tests**: Data structure and validation
- **Business Logic Tests**: Business rules and data consistency
- **Error Handling Tests**: Error scenarios and edge cases

## 🔧 Development

### Local Development Setup
```bash
# Quick start development environment
task quick-start

# Or manual setup
pip install -r requirements.txt
task up
task db-migrate
task db-create-tables

# Run quality checks
task quality
task test
```

### Development Toolbox
The project includes a comprehensive Taskfile.yml with **100+ automation tasks**:

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

See [TASKFILE.md](TASKFILE.md) for complete documentation.

### Code Quality Tools
- **Type Checking**: mypy with strict configuration
- **Linting**: ruff for fast Python linting
- **Formatting**: Automatic import organization
- **Testing**: pytest with async support

### Service Development
```python
from app.services import URLService
from app.models import URL

# Initialize service
url_service = URLService(session, generator_type="random")

# Create shortened URL
url = await url_service.create_short("https://example.com")

# Get URL by code (with caching)
url = await url_service.get_by_code("abc123")

# Soft delete URL
deleted_url = await url_service.delete(url)

# Restore deleted URL
restored_url = await url_service.restore(deleted_url)
```

## 📊 Monitoring & Observability

### Health Checks
- **Database**: Connection and query health
- **Redis**: Connection and operation health
- **RabbitMQ**: Connection and queue health
- **Application**: Overall service health

### Metrics
- **Response Times**: API endpoint latency
- **Cache Hit Rates**: Redis performance
- **Queue Depth**: RabbitMQ processing status
- **Database Connections**: Connection pool usage

### Logging
- **Structured Logging**: JSON format for central ingestion
- **Request Tracing**: End-to-end request tracking
- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Operation timing and resource usage

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head
```

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db

# Redis
REDIS_URL=redis://host:6379

# RabbitMQ
RABBITMQ_URL=amqp://user:pass@host:5672

# Security
SECRET_KEY=your-secret-key

# Application
ENVIRONMENT=production
DEBUG=false
```

### Scaling
- **Horizontal Scaling**: Multiple API instances behind load balancer
- **Database Scaling**: Read replicas for analytics queries
- **Cache Scaling**: Redis cluster for high availability
- **Queue Scaling**: Multiple worker instances for processing

## 📈 Performance

### Benchmarks
- **Redirect Latency**: < 10ms (with Redis cache)
- **API Response Time**: < 100ms
- **Throughput**: 1000+ requests/second
- **Cache Hit Rate**: 95%+ for active URLs

### Optimization Features
- **Redis Caching**: Sub-millisecond lookups
- **Async Processing**: Non-blocking visit logging
- **Connection Pooling**: Optimized database connections
- **Batch Processing**: Efficient worker processing

## 🔒 Security

### Security Features
- **Input Validation**: Comprehensive request validation
- **SQL Injection Protection**: Parameterized queries
- **Rate Limiting**: API rate limiting and protection
- **CORS Configuration**: Configurable cross-origin policies
- **Environment Isolation**: Secure configuration management

### Best Practices
- **Secrets Management**: Environment-based secret handling
- **TLS Encryption**: Encrypted connections for all services
- **Access Control**: Principle of least privilege
- **Audit Logging**: Comprehensive audit trails

## 📖 Documentation

### Additional Documentation
- **[SCALABILITY.md](SCALABILITY.md)**: Detailed scalability and performance strategy
- **[SERVICE_ORIENTED_DESIGN.md](SERVICE_ORIENTED_DESIGN.md)**: Architecture and design patterns
- **[TESTING.md](TESTING.md)**: Comprehensive testing strategy and coverage
- **[TASKFILE.md](TASKFILE.md)**: Complete development toolbox documentation
- **[API.md](API.md)**: Detailed API documentation and examples
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Production deployment and scaling guide
- **[CHANGELOG.md](CHANGELOG.md)**: Detailed changelog and improvements

### API Reference
- **OpenAPI Specification**: Available at `/openapi.json`
- **Interactive Docs**: Available at `/docs` and `/redoc`
- **Schema Validation**: Pydantic models with comprehensive validation

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run quality checks (`task typecheck`, `task lint`, `task test`)
5. Submit a pull request

### Code Standards
- **Type Safety**: All code must pass mypy validation
- **Testing**: New features require comprehensive tests
- **Documentation**: Update documentation for new features
- **Style**: Follow ruff linting rules

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent async web framework
- **SQLModel** for the modern ORM with type safety
- **Pydantic** for data validation and serialization
- **Redis** for high-performance caching
- **RabbitMQ** for reliable message queuing

---

**Built with ❤️ using modern Python and service-oriented architecture principles.**
