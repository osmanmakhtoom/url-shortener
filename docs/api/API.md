# API Documentation

This document provides comprehensive API documentation for the URL Shortener service.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

Currently, the API does not require authentication. Future versions may include API key authentication.

## Content Type

All requests and responses use `application/json` content type.

## Error Handling

The API uses standard HTTP status codes and returns error details in JSON format:

```json
{
  "detail": "Error message description"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Endpoints

### 1. Health Check

Check the health status of the service and its dependencies.

```http
GET /health
```

#### Response

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

#### Status Values

- `healthy`: All systems operational
- `degraded`: Some systems have issues but service is functional
- `unhealthy`: Critical systems are down

### 2. Root Endpoint

Get basic information about the service.

```http
GET /
```

#### Response

```json
{
  "message": "Welcome to URL Shortener",
  "version": "1.0.0",
  "environment": "development",
  "docs_url": "/docs",
  "redoc_url": "/redoc"
}
```

### 3. Shorten URL

Create a shortened URL from a long URL.

```http
POST /api/v1/shorten
```

#### Request Body

```json
{
  "url": "https://example.com"
}
```

#### Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | The URL to shorten (must be a valid HTTP/HTTPS URL) |

#### Response

```json
{
  "short_code": "abc123",
  "original_url": "https://example.com",
  "short_url": "/abc123",
  "created_at": "2023-01-01T00:00:00"
}
```

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `short_code` | string | The generated short code |
| `original_url` | string | The original URL that was shortened |
| `short_url` | string | The complete short URL path |
| `created_at` | string | ISO 8601 timestamp of creation |

#### Example Usage

```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 4. Redirect to Original URL

Redirect to the original URL using the short code.

```http
GET /{short_code}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `short_code` | string | Yes | The short code to redirect |

#### Response

- **Status Code**: `307 Temporary Redirect`
- **Location Header**: The original URL
- **Body**: Empty

#### Example Usage

```bash
curl -I "http://localhost:8000/abc123"
```

### 5. Get URL Statistics

Get statistics for a shortened URL.

```http
GET /api/v1/stats/{short_code}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `short_code` | string | Yes | The short code to get statistics for |

#### Response

```json
{
  "original_url": "https://example.com",
  "short_code": "abc123",
  "visit_count": 42,
  "created_at": "2023-01-01T00:00:00"
}
```

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `original_url` | string | The original URL that was shortened |
| `short_code` | string | The short code |
| `visit_count` | integer | Number of times the URL has been accessed |
| `created_at` | string | ISO 8601 timestamp of creation |

#### Example Usage

```bash
curl "http://localhost:8000/api/v1/stats/abc123"
```

## Data Models

### ShortenRequest

Request model for URL shortening.

```json
{
  "url": "https://example.com"
}
```

### ShortenResponse

Response model for URL shortening.

```json
{
  "short_code": "abc123",
  "original_url": "https://example.com",
  "short_url": "/abc123",
  "created_at": "2023-01-01T00:00:00"
}
```

### StatsResponse

Response model for URL statistics.

```json
{
  "original_url": "https://example.com",
  "short_code": "abc123",
  "visit_count": 42,
  "created_at": "2023-01-01T00:00:00"
}
```

### HealthCheck

Response model for health check.

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

## Rate Limiting

Currently, the API does not implement rate limiting. Future versions may include:

- Per-IP rate limiting
- Per-API-key rate limiting
- Burst protection
- DDoS protection

## Caching

The API uses Redis for caching to improve performance:

- **URL Lookups**: Cached for 24 hours
- **Statistics**: Cached for 5 minutes
- **Health Checks**: Cached for 30 seconds

## Analytics

The service tracks visit analytics:

- **Visit Logging**: Asynchronous visit logging via RabbitMQ
- **Visit Counting**: Real-time visit counting via Redis
- **Data Persistence**: Visit data persisted to PostgreSQL
- **Privacy**: IP addresses are logged but not exposed in API responses

## Short Code Generation

Short codes are generated using configurable strategies:

- **Random**: Random alphanumeric strings (default)
- **Sequential**: Sequential numeric codes
- **Custom**: Custom generation strategies

### Short Code Characteristics

- **Length**: 4-64 characters
- **Characters**: Alphanumeric and underscore/dash
- **Uniqueness**: Guaranteed unique across the system
- **Collision Handling**: Automatic retry on collision

## Error Responses

### Validation Errors

```json
{
  "detail": [
    {
      "loc": ["body", "url"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found Errors

```json
{
  "detail": "Not found"
}
```

### Server Errors

```json
{
  "detail": "Internal server error"
}
```

## Interactive Documentation

The API provides interactive documentation:

- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`

## SDK Examples

### Python

```python
import requests

# Shorten a URL
response = requests.post(
    "http://localhost:8000/api/v1/shorten",
    json={"url": "https://example.com"}
)
data = response.json()
print(f"Short URL: {data['short_url']}")

# Get statistics
stats = requests.get(f"http://localhost:8000/api/v1/stats/{data['short_code']}")
print(f"Visit count: {stats.json()['visit_count']}")
```

### JavaScript

```javascript
// Shorten a URL
const response = await fetch('http://localhost:8000/api/v1/shorten', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ url: 'https://example.com' })
});

const data = await response.json();
console.log(`Short URL: ${data.short_url}`);

// Get statistics
const stats = await fetch(`http://localhost:8000/api/v1/stats/${data.short_code}`);
const statsData = await stats.json();
console.log(`Visit count: ${statsData.visit_count}`);
```

### cURL

```bash
# Shorten a URL
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Get statistics
curl "http://localhost:8000/api/v1/stats/abc123"

# Health check
curl "http://localhost:8000/health"
```

## Webhooks

Currently, the API does not support webhooks. Future versions may include:

- Visit notification webhooks
- URL creation webhooks
- Error notification webhooks

## Versioning

The API uses URL versioning:

- **Current Version**: `v1`
- **Version Path**: `/api/v1/`
- **Backward Compatibility**: Maintained within major versions
- **Deprecation Policy**: 6-month notice for breaking changes

## Support

For API support and questions:

- **Documentation**: Check this documentation and interactive docs
- **Issues**: Report issues via GitHub issues
- **Community**: Join our community discussions

---

**Last Updated**: 2024-01-XX  
**API Version**: v1.0.0
