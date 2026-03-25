# 📍 Local Access Map - All Endpoints & Dashboards

**Project:** Wellness Solutions  
**Last Updated:** 2024-12-19

---

## 🎯 Primary Access Points

### Backend Services

| Service | URL | Purpose | Auth Required | Status |
|---------|-----|---------|---------------|--------|
| **Main Application** | http://localhost:8000 | Django web application | No (public pages) | ✅ |
| **Admin Panel** | http://localhost:8000/admin | Django admin interface | Yes (superuser) | ✅ |
| **API Base** | http://localhost:8000/api/ | REST API root | Token (most endpoints) | ✅ |
| **API Docs (Swagger)** | http://localhost:8000/api/docs/ | Interactive API documentation | Admin only | ✅ |
| **API Schema (JSON)** | http://localhost:8000/api/schema/ | OpenAPI schema | No | ✅ |

### Frontend Services

| Service | URL | Purpose | Auth Required | Status |
|---------|-----|---------|---------------|--------|
| **React App** | http://localhost:5173 | Frontend development server | No (public pages) | ✅ |
| **Vite HMR** | ws://localhost:5173 | Hot Module Replacement | No | ✅ |

### Monitoring & Tools

| Service | URL | Purpose | Auth Required | Status |
|---------|-----|---------|---------------|--------|
| **Flower** | http://localhost:5555 | Celery task monitor | admin / changeme | ⚠️ |
| **Mailpit UI** | http://localhost:8025 | Email testing interface | No | 🟡 |
| **Mailpit SMTP** | localhost:1025 | SMTP server for testing | No | 🟡 |

---

## 🔌 API Endpoints Reference

### Authentication Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/auth/register/` | POST | Register new user | No |
| `/api/auth/logout/` | POST | Logout user | Yes |
| `/api/auth-token/` | POST | Get authentication token | Yes |

### User Management

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/users/` | GET | List users | Yes |
| `/api/users/` | POST | Create user | Admin |
| `/api/users/{id}/` | GET | Get user details | Yes |
| `/api/users/{id}/` | PUT/PATCH | Update user | Yes (own) or Admin |

### Classes & Bookings

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/classes/` | GET | List classes | Yes |
| `/api/classes/` | POST | Create class | Admin/Instructor |
| `/api/classes/{id}/` | GET | Get class details | Yes |
| `/api/bookings/` | GET | List bookings | Yes |
| `/api/bookings/` | POST | Create booking | Yes |
| `/api/bookings/{id}/` | GET | Get booking details | Yes |
| `/api/bookings/{id}/` | PUT/PATCH | Update booking | Yes (own) or Admin |

### Analytics & Reports

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/analytics/` | GET | Get analytics data | Admin/Staff |
| `/api/instructor/classes/` | GET | Get instructor's classes | Instructor |

---

## 🌐 Frontend Routes

Based on `frontend/App.tsx` and routing configuration:

### Public Routes

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | Landing | Homepage |
| `/about` | About | About page |
| `/services` | Services | Services listing |
| `/pricing` | Pricing | Pricing information |
| `/schedule` | Schedule | Schedule view |
| `/contact` | Contact | Contact page |
| `/login` | Login | User login |
| `/register` | Register | User registration |

### Protected Routes

| Route | Component | Auth Required | Role |
|-------|-----------|---------------|------|
| `/dashboard` | Dashboard | Yes | All |
| `/dashboard/admin` | AdminDashboard | Yes | Admin |
| `/dashboard/instructor` | InstructorDashboard | Yes | Instructor |
| `/bookings` | Bookings | Yes | All |
| `/profile` | Profile | Yes | All |

---

## 🔐 Authentication Flow

### Token-Based API Authentication

1. **Login/Register** → Get token from `/api/auth-token/` or `/api/auth/register/`
2. **Store token** → `localStorage.setItem('authToken', token)`
3. **Include in requests** → Header: `Authorization: Token <token>`
4. **Logout** → Call `/api/auth/logout/` and remove token

### Django Session Authentication

- Used for web interface (admin, forms)
- CSRF protection enabled
- Session cookies: HttpOnly, SameSite=Strict

---

## 🗄️ Database Access

### PostgreSQL Connection

**From Host:**
```bash
psql -h localhost -p 5432 -U postgres -d wellness_solutions
```

**From Docker:**
```bash
docker-compose -f docker-compose.local.yml exec django python manage.py dbshell
```

**Connection String:**
```
postgres://postgres:postgres@localhost:5432/wellness_solutions
```

### Redis Connection

**From Host:**
```bash
redis-cli -h localhost -p 6379
# Select database 1
SELECT 1
```

**From Docker:**
```bash
docker-compose -f docker-compose.local.yml exec redis redis-cli
SELECT 1
```

---

## 📧 Email Testing (Mailpit)

### Access Mailpit UI
- **URL:** http://localhost:8025
- **Purpose:** View all emails sent by the application
- **Features:** 
  - View email content
  - Test email templates
  - Check email delivery

### SMTP Configuration
- **Host:** localhost
- **Port:** 1025
- **No authentication required**

---

## 🔍 Debugging Endpoints

### Django Debug Toolbar
- **URL:** http://localhost:8000/__debug__/
- **Available:** Only in DEBUG mode
- **Shows:** SQL queries, templates, request/response data

### Browser Reload
- **URL:** http://localhost:8000/__reload__/
- **Purpose:** Auto-reload on code changes

---

## 🧪 Testing Endpoints

### Health Check (if implemented)
```bash
curl http://localhost:8000/health/
```

### API Schema Validation
```bash
curl http://localhost:8000/api/schema/ | jq .
```

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Get token
curl -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test@example.com","password":"testpass123"}'

# Use token
curl http://localhost:8000/api/users/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## 📊 Monitoring Endpoints

### Flower (Celery Monitor)
- **URL:** http://localhost:5555
- **Username:** admin
- **Password:** changeme
- **Features:**
  - Active tasks
  - Task history
  - Worker status
  - Task statistics

---

## 🔄 WebSocket Endpoints (if implemented)

Currently, no WebSocket endpoints are configured. If real-time features are needed:
- Consider Django Channels
- WebSocket URL would typically be: `ws://localhost:8000/ws/`

---

## 🛡️ Security Notes

1. **CORS:** Configured for `localhost:5173` only
2. **CSRF:** Enabled for form submissions
3. **API Auth:** Token-based authentication required
4. **Admin:** Only accessible to superusers
5. **API Docs:** Only accessible to admin users

---

## 📱 Mobile/External Access

If accessing from another device on the same network:

1. **Find your IP:**
   ```bash
   hostname -I | awk '{print $1}'
   ```

2. **Update ALLOWED_HOSTS** in `.envs/.local/.django`:
   ```
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,YOUR_IP
   ```

3. **Access via:** `http://YOUR_IP:8000`

4. **Update frontend** `VITE_API_URL` to point to your IP

---

## 🚨 Common Issues

### "Connection Refused"
- Check service is running: `docker-compose ps`
- Check port is not blocked: `ss -tlnp | grep :8000`

### "CORS Error"
- Verify CORS_ALLOWED_ORIGINS includes your frontend URL
- Check browser console for exact error

### "403 Forbidden"
- Check authentication token is valid
- Verify user has required permissions
- Check CSRF token for form submissions

### "404 Not Found"
- Verify URL is correct
- Check URL routing in `config/urls.py`
- Ensure app is included in INSTALLED_APPS

---

**All endpoints are ready for local development!** 🎉

