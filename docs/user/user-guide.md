# 👥 User Guide

This guide explains how to use the URL Shortener service effectively.

## 🎯 Overview

The URL Shortener service allows you to:
- Create short URLs from long URLs
- Track visit statistics
- Access detailed analytics
- Manage your shortened URLs

## 🔗 Creating Short URLs

### Using the API

#### Basic URL Shortening

```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/very/long/url"}'
```

**Response:**
```json
{
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url",
  "short_url": "/abc123",
  "created_at": "2025-01-26T10:30:00Z"
}
```

#### Custom Short Codes

```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com", "custom_code": "my-link"}'
```

### Using the Web Interface

1. Visit http://localhost:8000/docs
2. Use the interactive API documentation
3. Try the `/api/v1/shorten` endpoint
4. Enter your URL and click "Execute"

## 📊 Viewing Statistics

### Get URL Statistics

```bash
curl "http://localhost:8000/api/v1/stats/abc123"
```

**Response:**
```json
{
  "original_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "visit_count": 42,
  "created_at": "2025-01-26T10:30:00Z"
}
```

### Understanding Statistics

- **visit_count**: Number of times the short URL has been accessed
- **created_at**: When the short URL was created
- **original_url**: The original long URL
- **short_code**: The generated short code

## 🔄 Accessing Short URLs

### Direct Access

Simply visit the short URL in your browser:
```
http://localhost:8000/abc123
```

The service redirects to the original URL.

### Programmatic Access

```bash
# Follow redirects automatically
curl -L "http://localhost:8000/abc123"

# Get redirect information without following
curl -I "http://localhost:8000/abc123"
```

## 🛡️ Security Features

### URL Validation

The service automatically validates URLs:
- Checks for valid URL format
- Ensures URLs are accessible
- Prevents malicious URLs

### Rate Limiting

- API calls are rate limited to prevent abuse
- Default: 100 requests per minute per IP
- Configurable limits for different endpoints

### Input Sanitization

- All inputs are sanitized and validated
- XSS protection for web interfaces
- SQL injection prevention

## 📈 Analytics and Monitoring

### Visit Tracking

Every access to a short URL is tracked:
- Timestamp of access
- IP address (anonymized)
- User agent information
- Geographic location (if available)

### Performance Metrics

- Response times
- Error rates
- Throughput statistics
- System health metrics

## 🔧 Configuration Options

### Environment Variables

Key configuration options:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/shortener

# Redis Cache
REDIS_URL=redis://localhost:6379

# RabbitMQ Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672

# Security
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
```

### Customization

- **Short Code Length**: Default 6 characters, configurable
- **Custom Domains**: Support for custom domains
- **Expiration**: Optional URL expiration dates
- **Password Protection**: Optional password protection for URLs

## 🚀 Performance

### Caching

- **Redis Caching**: Frequently accessed URLs are cached
- **Database Optimization**: Optimized queries for fast lookups
- **CDN Support**: Compatible with CDN services

### Scalability

- **Horizontal Scaling**: Supports multiple instances
- **Load Balancing**: Compatible with load balancers
- **Database Sharding**: Supports database sharding

## 📱 API Usage Examples

### Python Example

```python
import requests

# Create short URL
response = requests.post(
    "http://localhost:8000/api/v1/shorten",
    json={"url": "https://example.com/very/long/url"}
)
data = response.json()
short_code = data["short_code"]

# Get statistics
stats = requests.get(f"http://localhost:8000/api/v1/stats/{short_code}")
print(stats.json())
```

### JavaScript Example

```javascript
// Create short URL
const response = await fetch('http://localhost:8000/api/v1/shorten', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://example.com/very/long/url'
  })
});

const data = await response.json();
console.log('Short URL:', data.short_url);

// Get statistics
const stats = await fetch(`http://localhost:8000/api/v1/stats/${data.short_code}`);
const statsData = await stats.json();
console.log('Visit count:', statsData.visit_count);
```

### cURL Examples

```bash
# Create short URL
curl -X POST "http://localhost:8000/api/v1/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'

# Get statistics
curl "http://localhost:8000/api/v1/stats/abc123"

# Access short URL
curl -L "http://localhost:8000/abc123"
```

## 🔍 Troubleshooting

### Common Issues

#### URL Not Found (404)
- Check if the short code is correct
- Verify the URL hasn't expired
- Ensure the service is running

#### Invalid URL Error
- Check URL format (must include http:// or https://)
- Ensure URL is accessible
- Verify URL is not blocked

#### Rate Limit Exceeded
- Wait before making more requests
- Consider implementing request queuing
- Contact administrator for limit increases

### Error Codes

- **400**: Bad Request - Invalid input
- **404**: Not Found - Short URL doesn't exist
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Server issue

## 📞 Support

### Getting Help

- **Documentation**: [Complete Documentation](../README.md)
- **API Docs**: http://localhost:8000/docs
- **Issues**: [GitHub Issues](https://github.com/osmanmakhtoom/url-shortener/issues)
- **Email**: osmanmakhtoom@gmail.com

### Reporting Issues

When reporting issues, include:
- Short code or URL that's not working
- Error messages received
- Steps to reproduce the issue
- Expected vs actual behavior

## 🎯 Best Practices

### URL Management

- Use descriptive custom codes when possible
- Monitor your URL statistics regularly
- Keep track of important short URLs
- Consider URL expiration for temporary links

### Security

- Don't share sensitive information in URLs
- Use HTTPS for all requests
- Monitor for suspicious activity
- Regularly review your URL statistics

### Performance

- Use caching for frequently accessed URLs
- Implement proper error handling
- Monitor response times
- Use appropriate timeouts

---

**Happy URL shortening!** 🚀

For more advanced usage and development information, see the [Developer Documentation](../developer/development-setup.md).
