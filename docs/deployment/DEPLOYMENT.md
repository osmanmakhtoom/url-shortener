# Deployment Guide

This guide covers deployment strategies for the URL Shortener service, from local development to production environments.

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- Basic knowledge of containerization

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd url_shortener

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend python -m alembic upgrade head

# Verify deployment
curl http://localhost:8000/health
```

## 🏗️ Architecture Overview

### Service Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   PostgreSQL    │    │     Redis       │
│   (Port 8000)   │◄──►│   (Port 5432)   │    │   (Port 6379)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RabbitMQ      │    │   Nginx         │    │   Workers       │
│   (Port 5672)   │    │   (Port 80)     │    │   (Background)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Queue**: RabbitMQ 3.12+
- **Web Server**: Nginx (production)
- **Containerization**: Docker & Docker Compose

## 🐳 Docker Deployment

### Development Environment

#### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

#### 2. Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Check service status
docker-compose ps
```

#### 3. Database Initialization

```bash
# Run migrations
docker-compose exec backend python -m alembic upgrade head

# Or create tables directly (development only)
docker-compose exec backend python app/management.py create-tables
```

#### 4. Verify Deployment

```bash
# Health check
curl http://localhost:8000/health

# Test API
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Production Environment

#### 1. Production Configuration

```bash
# Create production environment file
cp .env.example .env.prod

# Edit production settings
nano .env.prod
```

#### 2. Production Environment Variables

```bash
# Database
DATABASE_URL=postgresql+psycopg://user:password@postgres:5432/url_shortener
POSTGRES_DB=url_shortener
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password

# Redis
REDIS_URL=redis://redis:6379

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672

# Application
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secure-secret-key
VERSION=1.0.0

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

#### 3. Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head

# Verify deployment
curl https://your-domain.com/health
```

## ☁️ Cloud Deployment

### AWS Deployment

#### 1. ECS with Fargate

```yaml
# docker-compose.aws.yml
version: '3.8'
services:
  backend:
    image: your-registry/url-shortener:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - RABBITMQ_URL=${RABBITMQ_URL}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - rabbitmq

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  rabbitmq:
    image: rabbitmq:3.12-management
    environment:
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_USER}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
```

#### 2. RDS and ElastiCache

```bash
# Use managed services
DATABASE_URL=postgresql+psycopg://user:pass@your-rds-endpoint:5432/url_shortener
REDIS_URL=redis://your-elasticache-endpoint:6379
```

### Google Cloud Platform

#### 1. Cloud Run

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/url-shortener', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/url-shortener']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'url-shortener', '--image', 'gcr.io/$PROJECT_ID/url-shortener', '--platform', 'managed', '--region', 'us-central1']
```

#### 2. Cloud SQL and Memorystore

```bash
# Use managed services
DATABASE_URL=postgresql+psycopg://user:pass@/cloudsql/project:region:instance/dbname
REDIS_URL=redis://your-memorystore-endpoint:6379
```

### Azure Deployment

#### 1. Container Instances

```yaml
# azure-container-instances.yml
apiVersion: 2018-10-01
location: eastus
name: url-shortener
properties:
  containers:
  - name: url-shortener
    properties:
      image: your-registry/url-shortener:latest
      resources:
        requests:
          cpu: 1
          memoryInGb: 2
      ports:
      - port: 8000
        protocol: TCP
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: TCP
      port: 8000
```

#### 2. Azure Database and Cache

```bash
# Use managed services
DATABASE_URL=postgresql+psycopg://user:pass@your-azure-postgres:5432/url_shortener
REDIS_URL=redis://your-azure-redis:6380
```

## 🔧 Configuration

### Environment Variables

#### Required Variables

```bash
# Database
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db

# Cache
REDIS_URL=redis://host:6379

# Queue
RABBITMQ_URL=amqp://user:pass@host:5672

# Application
ENVIRONMENT=production
SECRET_KEY=your-secret-key
```

#### Optional Variables

```bash
# Application
DEBUG=false
VERSION=1.0.0
PROJECT_NAME=URL Shortener

# Security
ALLOWED_HOSTS=your-domain.com
CORS_ORIGINS=https://your-domain.com

# Performance
WORKERS=4
MAX_CONNECTIONS=100
```

### Database Configuration

#### PostgreSQL Settings

```sql
-- Performance tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Reload configuration
SELECT pg_reload_conf();
```

#### Connection Pooling

```python
# Database connection settings
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 30
DATABASE_POOL_TIMEOUT = 30
DATABASE_POOL_RECYCLE = 3600
```

### Redis Configuration

#### Redis Settings

```conf
# redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

#### Cache Configuration

```python
# Cache settings
CACHE_TTL = 86400  # 24 hours
CACHE_MAX_CONNECTIONS = 100
CACHE_RETRY_ATTEMPTS = 3
CACHE_RETRY_DELAY = 1
```

### RabbitMQ Configuration

#### RabbitMQ Settings

```conf
# rabbitmq.conf
vm_memory_high_watermark.relative = 0.6
disk_free_limit.relative = 2.0
heartbeat = 60
```

#### Queue Configuration

```python
# Queue settings
QUEUE_PREFETCH_COUNT = 10
QUEUE_DURABLE = True
QUEUE_AUTO_DELETE = False
QUEUE_TTL = 3600000  # 1 hour
```

## 📊 Monitoring & Observability

### Health Checks

#### Application Health

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed health check
curl http://localhost:8000/health | jq
```

#### Service Health

```bash
# Database health
docker-compose exec postgres pg_isready

# Redis health
docker-compose exec redis redis-cli ping

# RabbitMQ health
docker-compose exec rabbitmq rabbitmq-diagnostics ping
```

### Logging

#### Application Logs

```bash
# View application logs
docker-compose logs -f backend

# View specific service logs
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f rabbitmq
```

#### Log Configuration

```python
# Logging configuration
LOGGING_LEVEL = "INFO"
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_FILE = "/var/log/url-shortener.log"
```

### Metrics

#### Application Metrics

```python
# Metrics endpoints
METRICS_ENABLED = True
METRICS_PORT = 9090
METRICS_PATH = "/metrics"
```

#### System Metrics

```bash
# Container metrics
docker stats

# System metrics
htop
iostat
netstat
```

## 🔒 Security

### SSL/TLS Configuration

#### Nginx SSL

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Security Headers

```python
# Security middleware
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'"
}
```

### Access Control

#### Firewall Configuration

```bash
# UFW configuration
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### Network Security

```yaml
# docker-compose.yml
services:
  backend:
    networks:
      - app-network
    ports:
      - "127.0.0.1:8000:8000"  # Bind to localhost only

networks:
  app-network:
    driver: bridge
    internal: true
```

## 🚀 Scaling

### Horizontal Scaling

#### Load Balancer Configuration

```nginx
# nginx.conf
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

#### Auto-scaling

```yaml
# kubernetes-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: url-shortener
spec:
  replicas: 3
  selector:
    matchLabels:
      app: url-shortener
  template:
    metadata:
      labels:
        app: url-shortener
    spec:
      containers:
      - name: url-shortener
        image: your-registry/url-shortener:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: url-shortener-service
spec:
  selector:
    app: url-shortener
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Vertical Scaling

#### Resource Optimization

```python
# Resource configuration
WORKERS = 4
MAX_CONNECTIONS = 100
MEMORY_LIMIT = "512MB"
CPU_LIMIT = "500m"
```

#### Database Scaling

```sql
-- Read replicas
CREATE SUBSCRIPTION replica_subscription
CONNECTION 'host=replica-server port=5432 user=replica_user dbname=url_shortener'
PUBLICATION main_publication;
```

## 🔄 Backup & Recovery

### Database Backup

```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/url_shortener_$DATE.sql"

# Create backup
docker-compose exec postgres pg_dump -U postgres url_shortener > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

### Redis Backup

```bash
# Redis backup
docker-compose exec redis redis-cli BGSAVE
docker cp $(docker-compose ps -q redis):/data/dump.rdb ./redis-backup-$(date +%Y%m%d).rdb
```

### Application Backup

```bash
# Application data backup
tar -czf app-backup-$(date +%Y%m%d).tar.gz \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  .
```

## 🧪 Testing in Production

### Smoke Tests

```bash
# Basic functionality test
curl -f http://localhost:8000/health || exit 1

# API functionality test
SHORT_URL=$(curl -s -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | jq -r '.short_url')

curl -f "http://localhost:8000$SHORT_URL" || exit 1
```

### Load Testing

```bash
# Install artillery
npm install -g artillery

# Run load test
artillery run load-test.yml
```

```yaml
# load-test.yml
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: "URL shortening"
    weight: 70
    flow:
      - post:
          url: "/api/v1/shorten"
          json:
            url: "https://example.com/{{ $randomString() }}"
  - name: "Health check"
    weight: 30
    flow:
      - get:
          url: "/health"
```

## 📋 Maintenance

### Regular Maintenance Tasks

#### Daily

- Monitor health endpoints
- Check error logs
- Verify backup completion
- Monitor resource usage

#### Weekly

- Review performance metrics
- Update dependencies
- Clean old logs
- Test disaster recovery

#### Monthly

- Security updates
- Performance optimization
- Capacity planning
- Documentation updates

### Update Procedures

#### Application Updates

```bash
# Pull latest changes
git pull origin main

# Build new image
docker-compose build backend

# Rolling update
docker-compose up -d --no-deps backend

# Verify update
curl http://localhost:8000/health
```

#### Database Updates

```bash
# Run migrations
docker-compose exec backend python -m alembic upgrade head

# Verify migration
docker-compose exec postgres psql -U postgres -d url_shortener -c "\dt"
```

## 🆘 Troubleshooting

### Common Issues

#### Service Won't Start

```bash
# Check logs
docker-compose logs backend

# Check configuration
docker-compose config

# Restart services
docker-compose restart
```

#### Database Connection Issues

```bash
# Test database connection
docker-compose exec backend python -c "
import asyncio
from app.core.db import engine
asyncio.run(engine.connect())
"

# Check database status
docker-compose exec postgres pg_isready
```

#### Redis Connection Issues

```bash
# Test Redis connection
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis
```

#### RabbitMQ Connection Issues

```bash
# Test RabbitMQ connection
docker-compose exec rabbitmq rabbitmq-diagnostics ping

# Check RabbitMQ status
docker-compose exec rabbitmq rabbitmq-diagnostics status
```

### Performance Issues

#### High Response Times

```bash
# Check resource usage
docker stats

# Check database performance
docker-compose exec postgres psql -U postgres -d url_shortener -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
"
```

#### Memory Issues

```bash
# Check memory usage
free -h
docker stats

# Check Redis memory
docker-compose exec redis redis-cli info memory
```

### Recovery Procedures

#### Database Recovery

```bash
# Restore from backup
docker-compose exec postgres psql -U postgres -d url_shortener < backup.sql

# Verify restoration
docker-compose exec postgres psql -U postgres -d url_shortener -c "\dt"
```

#### Application Recovery

```bash
# Restart all services
docker-compose down
docker-compose up -d

# Verify recovery
curl http://localhost:8000/health
```

---

**This deployment guide provides comprehensive instructions for deploying the URL Shortener service in various environments. For additional support, refer to the troubleshooting section or contact the development team.**
