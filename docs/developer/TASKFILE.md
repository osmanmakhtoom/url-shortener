# Taskfile.yml - Development Toolbox

This document provides a comprehensive guide to the Taskfile.yml automation toolbox for the URL Shortener project.

## 🎯 Overview

The Taskfile.yml provides a complete automation toolbox with **100+ tasks** organized into logical categories for development, testing, deployment, and maintenance.

## 📋 Quick Reference

### Essential Commands
```bash
# Quick start development environment
task quick-start

# Run all quality checks and tests
task quick-test

# Complete development workflow
task workflow-dev

# Show all available tasks
task help
```

## 🐳 Docker & Infrastructure

### Container Management
```bash
# Build and start all services
task up

# Start services in background
task up-detached

# Stop all services and remove volumes
task down

# Stop services but keep volumes
task down-keep-volumes

# Restart all services
task restart

# Restart only backend service
task restart-backend
```

### Logging & Monitoring
```bash
# View all service logs
task logs

# View specific service logs
task logs-backend
task logs-db
task logs-redis
task logs-rabbitmq

# Show service status
task status

# Check service health
task health
```

### Shell Access
```bash
# Open backend shell
task shell

# Open database shell
task shell-db

# Open Redis CLI
task shell-redis

# Open RabbitMQ management
task shell-rabbitmq
```

## 🗄️ Database Operations

### Migrations
```bash
# Run database migrations
task db-migrate

# Create new migration
task db-makemigration "Add user table"

# Show migration history
task db-history

# Show current revision
task db-current

# Downgrade by one revision
task db-downgrade

# Downgrade to specific revision
task db-downgrade-to "abc123"
```

### Database Management
```bash
# Create tables directly (development)
task db-create-tables

# Reset database (drop and recreate)
task db-reset

# Show all tables
task db-show-tables

# Show applied migrations
task db-show-migrations

# Analyze database performance
task db-analyze
```

### Backup & Restore
```bash
# Create database backup
task db-backup

# Restore from backup
task db-restore backup_20240101_120000.sql

# Create complete backup
task backup-all

# Restore from complete backup
task restore-all backup_file.sql
```

## 🧪 Testing & Quality

### Test Execution
```bash
# Run all tests
task test

# Run tests with verbose output
task test-verbose

# Run specific test file
task test-specific tests/test_services.py

# Run only failed tests
task test-failed

# Run all test categories
task test-all-categories
```

### Test Categories
```bash
# Service layer tests
task test-services

# Integration tests
task test-integration

# Business logic tests
task test-business-logic

# Validation and schema tests
task test-validation

# Performance tests
task test-performance
```

### Coverage & Quality
```bash
# Run tests with coverage
task test-coverage

# Run tests with coverage and fail if below threshold
task test-coverage-fail

# Generate coverage badge (coverage.svg)
task test-coverage-badge

# Run all quality checks
task quality

# Auto-fix quality issues
task quality-fix
```

### Code Quality
```bash
# Run linting
task lint

# Run linting with detailed output
task lint-verbose

# Auto-fix linting issues
task lint-fix

# Format code
task format

# Check code formatting
task format-check

# Run type checking
task typecheck

# Run strict type checking
task typecheck-strict
```

## 🚀 Development Workflow

### Environment Setup
```bash
# Complete development setup
task dev-setup

# Reset development environment
task dev-reset

# Clean development environment
task dev-clean

# Show development status
task dev-status
```

### Quick Actions
```bash
# Quick start (setup + test)
task quick-start

# Quick test (quality + test)
task quick-test

# Quick deploy (quality + test + deploy)
task quick-deploy
```

## 🔧 API & Service Management

### API Testing
```bash
# Test API endpoints
task api-test

# Show API documentation URLs
task api-docs
```

### Service Management
```bash
# Start background workers
task workers-start

# Check worker status
task workers-status

# Clear Redis cache
task cache-clear

# Show Redis cache info
task cache-info

# Show RabbitMQ queue info
task queue-info
```

## 🚀 Deployment & Production

### Deployment
```bash
# Deploy to development
task deploy-dev

# Deploy to production
task deploy-prod

# Check deployment health
task deploy-check
```

### Monitoring
```bash
# Show real-time monitoring
task monitor

# Monitor logs in real-time
task monitor-logs

# Show application metrics
task metrics

# Run performance tests
task performance-test
```

## 🛠️ Utilities & Helpers

### Maintenance
```bash
# Clean up Docker resources
task clean

# Clean up all Docker resources
task clean-all

# Update Python dependencies
task update-deps

# Run security scan
task security-scan
```

### Information
```bash
# Show project information
task info

# Show version information
task version

# Show environment information
task env
```

### Custom Commands
```bash
# Run custom command
task custom "your-command-here"

# Execute command in backend container
task exec "python -c 'print(\"Hello World\")'"
```

## 🎮 Interactive Modes

### Interactive Development
```bash
# Enter interactive development mode
task interactive

# Enter debug mode
task debug
```

## 🔄 Workflow Shortcuts

### Complete Workflows
```bash
# Development workflow
task workflow-dev

# CI/CD workflow
task workflow-ci

# Deployment workflow
task workflow-deploy
```

## 📊 Task Categories Summary

### 🐳 Infrastructure (20 tasks)
- Container management
- Logging and monitoring
- Shell access
- Health checks

### 🗄️ Database (15 tasks)
- Migrations
- Database management
- Backup and restore
- Performance analysis

### 🧪 Testing (20 tasks)
- Test execution
- Test categories
- Coverage reporting
- Quality checks

### 🔧 Development (10 tasks)
- Environment setup
- Quick actions
- Development workflows

### 🚀 Deployment (10 tasks)
- Deployment strategies
- Monitoring
- Production management

### 🛠️ Utilities (15 tasks)
- Maintenance
- Information
- Custom commands
- Security

### 🎮 Interactive (5 tasks)
- Interactive modes
- Debug tools

### 🔄 Workflows (5 tasks)
- Complete workflows
- CI/CD pipelines

## 🎯 Best Practices

### Daily Development
```bash
# Start your day
task quick-start

# During development
task quality
task test

# End of day
task dev-status
```

### Before Committing
```bash
# Run complete quality check
task quality
task test-coverage-fail
task security-scan
```

### Before Deployment
```bash
# Run deployment workflow
task workflow-deploy
```

### Troubleshooting
```bash
# Check service health
task health

# View logs
task logs

# Check database status
task db-current

# Monitor performance
task monitor
```

## 🔧 Customization

### Adding New Tasks
To add new tasks, edit the `Taskfile.yml` file and add them to the appropriate category:

```yaml
your-new-task:
  desc: Description of your task
  cmds:
    - command1
    - command2
```

### Environment Variables
The Taskfile uses these environment variables:
- `PROJECT_NAME`: Project name
- `BACKEND_SERVICE`: Backend service name
- `DB_SERVICE`: Database service name
- `REDIS_SERVICE`: Redis service name
- `RABBITMQ_SERVICE`: RabbitMQ service name
- `NGINX_SERVICE`: Nginx service name

### Task Dependencies
Tasks can depend on other tasks using the `deps` keyword:

```yaml
your-task:
  deps: [other-task]
  cmds:
    - your-command
```

## 📚 Examples

### Complete Development Session
```bash
# Start development
task quick-start

# Make changes to code
# ... edit files ...

# Check quality
task quality

# Run tests
task test

# Test API
task api-test

# Check status
task dev-status
```

### Database Migration Workflow
```bash
# Create migration
task db-makemigration "Add new feature"

# Review migration
task db-history

# Apply migration
task db-migrate

# Verify migration
task db-current
task db-show-tables
```

### Production Deployment
```bash
# Run quality checks
task quality

# Run tests
task test-coverage-fail

# Deploy to production
task deploy-prod

# Verify deployment
task deploy-check
```

## 🆘 Troubleshooting

### Common Issues

#### Task Not Found
```bash
# List all available tasks
task help

# Check task syntax
task --list
```

#### Docker Issues
```bash
# Check service status
task status

# View logs
task logs

# Restart services
task restart
```

#### Database Issues
```bash
# Check database health
task health

# View database logs
task logs-db

# Check migration status
task db-current
```

#### Test Issues
```bash
# Run specific test
task test-specific tests/test_specific.py

# Run failed tests only
task test-failed

# Check test coverage
task test-coverage
```

## 🎉 Conclusion

The Taskfile.yml provides a comprehensive automation toolbox with **100+ tasks** covering every aspect of development, testing, deployment, and maintenance. Use `task help` to see all available tasks and their descriptions.

---

**The URL Shortener development toolbox is ready for use!** 🚀
