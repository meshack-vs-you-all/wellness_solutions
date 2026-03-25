# Wellness Solutions - Complete Test Flow 🧪

## 📋 API Documentation & Endpoints

### Available API Endpoints:
- **API Documentation (Swagger)**: http://localhost:8000/api/docs/ (requires auth)
- **API Schema**: http://localhost:8000/api/schema/
- **User API**: `/api/users/` (CRUD operations)
- **Auth Token**: `/api/auth-token/` (DRF token authentication)
- **Current User**: `/api/users/me/` (get current user info)

### Frontend Integration Points:
1. **Authentication**: Use `/api/auth-token/` for token-based auth
2. **User Management**: Full REST API at `/api/users/`
3. **OpenAPI Schema**: Available at `/api/schema/` for auto-generating client SDKs

---

## ✅ Complete Test Flow

### 1. **Basic Site Access**
```bash
# Test home page
curl -I http://localhost:8000
# Expected: HTTP 200 OK

# Test about page
curl -I http://localhost:8000/about/
# Expected: HTTP 200 OK
```

### 2. **Admin Panel Access**
```bash
# Access admin panel
echo "Visit: http://localhost:8000/admin"
echo "Login with: admin@example.com / admin123"
```

### 3. **User Registration Flow**
```bash
# Test registration page
curl -I http://localhost:8000/accounts/signup/
# Expected: HTTP 200 OK
```

### 4. **Email Testing with Mailpit**
```bash
# Check email interface
echo "Visit: http://localhost:8025"
echo "Any emails sent by the app will appear here"
```

### 5. **API Authentication Test**
```bash
# Get auth token
curl -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

### 6. **API User Endpoints Test**
```bash
# First get the token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}' | python -c "import sys, json; print(json.load(sys.stdin).get('token', ''))")

# Test authenticated API access
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/users/me/
```

### 7. **Database Connectivity Test**
```bash
# Check database migrations
docker exec wellness_solutions_local_django python manage.py showmigrations
```

### 8. **Celery & Background Tasks**
```bash
# Check Celery workers
docker logs wellness_solutions_local_celeryworker --tail 10

# Access Flower monitoring
echo "Visit: http://localhost:5555"
```

### 9. **Static Files Test**
```bash
# Check static files are served
curl -I http://localhost:8000/static/css/project.css
# Expected: HTTP 200 OK
```

### 10. **Create Test User via Django Shell**
```bash
docker exec -it wellness_solutions_local_django python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
test_user = User.objects.create_user(email='test@example.com', password='testpass123')
print(f"Created test user: {test_user.email}")
EOF
```

---

## 🚀 Quick Automated Test Script

Run this complete test flow:

```bash
#!/bin/bash
echo "🧪 Starting Wellness Solutions Test Flow..."
echo "========================================"

# 1. Check all containers are running
echo -e "\n✅ Checking Docker containers..."
docker ps --format "table {{.Names}}\t{{.Status}}" | grep jpf_stretch

# 2. Test home page
echo -e "\n✅ Testing home page..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200"; then
    echo "Home page: OK ✓"
else
    echo "Home page: FAILED ✗"
fi

# 3. Test admin page
echo -e "\n✅ Testing admin page..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/ | grep -q "302\|200"; then
    echo "Admin page: OK ✓"
else
    echo "Admin page: FAILED ✗"
fi

# 4. Test API auth
echo -e "\n✅ Testing API authentication..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}' | python -c "import sys, json; data = json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)

if [ ! -z "$TOKEN" ]; then
    echo "API Auth: OK ✓ (Token retrieved)"
else
    echo "API Auth: FAILED ✗"
fi

# 5. Test authenticated API endpoint
echo -e "\n✅ Testing authenticated API access..."
if [ ! -z "$TOKEN" ]; then
    API_RESPONSE=$(curl -s -w "\n%{http_code}" -H "Authorization: Token $TOKEN" http://localhost:8000/api/users/me/)
    HTTP_CODE=$(echo "$API_RESPONSE" | tail -n 1)
    if [ "$HTTP_CODE" = "200" ]; then
        echo "API Access: OK ✓"
    else
        echo "API Access: FAILED ✗ (HTTP $HTTP_CODE)"
    fi
fi

# 6. Check Mailpit
echo -e "\n✅ Testing email service (Mailpit)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8025 | grep -q "200"; then
    echo "Mailpit: OK ✓"
else
    echo "Mailpit: FAILED ✗"
fi

# 7. Check Flower
echo -e "\n✅ Testing Celery monitoring (Flower)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5555 | grep -q "200"; then
    echo "Flower: OK ✓"
else
    echo "Flower: FAILED ✗"
fi

# 8. Database check
echo -e "\n✅ Testing database connectivity..."
if docker exec wellness_solutions_local_django python manage.py dbshell -c "SELECT 1;" 2>/dev/null | grep -q "1"; then
    echo "Database: OK ✓"
else
    echo "Database: FAILED ✗"
fi

echo -e "\n========================================"
echo "🎉 Test flow complete!"
echo ""
echo "📝 Manual verification URLs:"
echo "  - Main app: http://localhost:8000"
echo "  - Admin: http://localhost:8000/admin (admin@example.com/admin123)"
echo "  - API Docs: http://localhost:8000/api/docs/ (requires login)"
echo "  - Emails: http://localhost:8025"
echo "  - Celery: http://localhost:5555"
```

---

## 🔌 Frontend Integration Guide

### For React/Vue/Angular Frontend:

1. **Generate TypeScript Client from OpenAPI:**
```bash
# Get the OpenAPI schema (after auth)
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/schema/ > openapi.json

# Use openapi-generator to create client
npx @openapitools/openapi-generator-cli generate \
  -i openapi.json \
  -g typescript-axios \
  -o ./frontend/src/api
```

2. **Authentication Setup:**
```javascript
// Frontend auth service example
const API_BASE = 'http://localhost:8000';

async function login(email, password) {
  const response = await fetch(`${API_BASE}/api/auth-token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('authToken', data.token);
  return data.token;
}

// Use token in requests
const token = localStorage.getItem('authToken');
fetch(`${API_BASE}/api/users/me/`, {
  headers: { 'Authorization': `Token ${token}` }
});
```

3. **CORS Configuration:**
The app already has `django-cors-headers` installed. Configure allowed origins in settings if needed.

---

## 📱 Mobile App Integration

For React Native or Flutter apps, use the same API endpoints with token authentication:

```dart
// Flutter example
final response = await http.post(
  Uri.parse('http://YOUR_SERVER_IP:8000/api/auth-token/'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'email': email, 'password': password}),
);
```

Remember to use your machine's IP address instead of localhost for mobile testing.
