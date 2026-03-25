# 🚀 RUN EVERYTHING NOW - Final Launch Guide

**Last Updated:** 2024-12-19  
**Status:** ✅ Ready to Launch (with port conflict resolution)

---

## ⚡ Quick Start (Choose Your Path)

### Path A: Use Existing Services (Recommended - No Conflicts)

If you have existing `postgres`, `redis`, and `mailpit` containers running:

```bash
# 1. Update environment to use existing services
cat > .envs/.local/.postgres << 'EOF'
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5432
POSTGRES_DB=wellness_solutions
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-existing-postgres-password
DATABASE_URL=postgres://postgres:your-existing-postgres-password@host.docker.internal:5432/wellness_solutions
EOF

# 2. Update Redis URL
sed -i 's|REDIS_URL=redis://redis:6379/1|REDIS_URL=redis://host.docker.internal:6379/1|' .envs/.local/.django

# 3. Start only Django and Celery services
docker-compose -f docker-compose.local.yml up django celeryworker celerybeat flower --build -d

# 4. Run migrations
docker-compose -f docker-compose.local.yml exec django python manage.py migrate

# 5. Create superuser
docker-compose -f docker-compose.local.yml exec django python manage.py createsuperuser

# 6. Start frontend
cd frontend && pnpm install && pnpm dev
```

### Path B: Use Different Ports (Isolated Services)

If you want separate services on different ports:

```bash
# 1. Copy override file
cp docker-compose.local.override.yml.example docker-compose.local.override.yml

# 2. Update environment files for new ports
sed -i 's|POSTGRES_PORT=5432|POSTGRES_PORT=5432|' .envs/.local/.postgres
# Note: Internal port stays 5432, only host port changes

# 3. Update .envs/.local/.postgres DATABASE_URL if needed
# (Keep internal port as 5432, Docker handles mapping)

# 4. Start all services
docker-compose -f docker-compose.local.yml -f docker-compose.local.override.yml up --build -d

# 5. Run migrations
docker-compose -f docker-compose.local.yml -f docker-compose.local.override.yml exec django python manage.py migrate

# 6. Create superuser
docker-compose -f docker-compose.local.yml -f docker-compose.local.override.yml exec django python manage.py createsuperuser

# 7. Start frontend
cd frontend && pnpm install && pnpm dev
```

### Path C: Full Docker Stack (All Services)

If ports 5432, 6379, 8025, 1025 are available:

```bash
# 1. Start everything
docker-compose -f docker-compose.local.yml up --build -d

# 2. Wait for services to be ready (30 seconds)
sleep 30

# 3. Run migrations
docker-compose -f docker-compose.local.yml exec django python manage.py migrate

# 4. Create superuser
docker-compose -f docker-compose.local.yml exec django python manage.py createsuperuser

# 5. Collect static files
docker-compose -f docker-compose.local.yml exec django python manage.py collectstatic --noinput

# 6. Start frontend (separate terminal)
cd frontend && pnpm install && pnpm dev
```

---

## 📋 Pre-Flight Checklist

Before running, verify:

- [ ] Environment files exist: `.envs/.local/.django` and `.envs/.local/.postgres`
- [ ] Port conflicts resolved (see Port Safety Matrix below)
- [ ] Docker is running: `docker ps`
- [ ] Node.js 20+ installed: `node --version`
- [ ] pnpm installed: `pnpm --version` (or use npm)

---

## 🔍 Verification Steps

After starting services, verify everything works:

```bash
# 1. Check all containers are running
docker-compose -f docker-compose.local.yml ps

# 2. Test backend API
curl http://localhost:8000/api/schema/ | head -20

# 3. Test database connection
docker-compose -f docker-compose.local.yml exec django python manage.py dbshell -c "\dt"

# 4. Test Redis connection
docker-compose -f docker-compose.local.yml exec django python -c "import redis; r = redis.from_url('redis://redis:6379/1'); print('✅ Redis OK' if r.ping() else '❌ Redis FAIL')"

# 5. Check Celery workers
docker-compose -f docker-compose.local.yml exec django celery -A config.celery_app inspect active

# 6. Test frontend (should return HTML)
curl http://localhost:5173 | head -20
```

---

## 🌐 Access URLs

Once running, access these URLs:

| Service | URL | Credentials |
|---------|-----|------------|
| **Django Backend** | http://localhost:8000 | - |
| **Django Admin** | http://localhost:8000/admin | (create superuser) |
| **API Docs** | http://localhost:8000/api/docs/ | Admin only |
| **API Schema** | http://localhost:8000/api/schema/ | - |
| **Frontend** | http://localhost:5173 | - |
| **Flower** | http://localhost:5555 | admin / changeme |
| **Mailpit** | http://localhost:8025 | - |

---

## 🛠️ Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8000
# or
ss -tlnp | grep :8000

# Stop conflicting service or use different port
```

### Database Connection Failed

```bash
# Check postgres is accessible
docker-compose -f docker-compose.local.yml exec django python -c "import psycopg2; psycopg2.connect('postgres://postgres:postgres@postgres:5432/wellness_solutions')"

# Check environment variables
docker-compose -f docker-compose.local.yml exec django env | grep POSTGRES
```

### Redis Connection Failed

```bash
# Test Redis
docker-compose -f docker-compose.local.yml exec django python -c "import redis; r = redis.from_url('redis://redis:6379/1'); r.ping()"

# Check Redis URL
docker-compose -f docker-compose.local.yml exec django env | grep REDIS
```

### Frontend Can't Connect to Backend

1. Check CORS settings in `config/settings/local.py`
2. Verify `VITE_API_URL` in frontend (should be `http://localhost:8000/api`)
3. Check browser console for CORS errors
4. Verify backend is running: `curl http://localhost:8000/api/schema/`

### Celery Not Working

```bash
# Check Celery worker logs
docker-compose -f docker-compose.local.yml logs celeryworker

# Check Redis connection from Celery
docker-compose -f docker-compose.local.yml exec celeryworker celery -A config.celery_app inspect ping
```

---

## 📊 Service Status Commands

```bash
# View all logs
docker-compose -f docker-compose.local.yml logs -f

# View specific service logs
docker-compose -f docker-compose.local.yml logs -f django
docker-compose -f docker-compose.local.yml logs -f celeryworker

# Check service status
docker-compose -f docker-compose.local.yml ps

# Restart a service
docker-compose -f docker-compose.local.yml restart django

# Stop all services
docker-compose -f docker-compose.local.yml down

# Stop and remove volumes (⚠️ deletes data)
docker-compose -f docker-compose.local.yml down -v
```

---

## 🔐 First-Time Setup

After starting services for the first time:

```bash
# 1. Create superuser
docker-compose -f docker-compose.local.yml exec django python manage.py createsuperuser

# 2. Load initial data (if fixtures exist)
docker-compose -f docker-compose.local.yml exec django python manage.py loaddata initial_data

# 3. Create test organizations/locations (if needed)
docker-compose -f docker-compose.local.yml exec django python manage.py shell
# Then in shell:
# from services.models import Organization, Location
# org = Organization.objects.create(name="Test Org")
# Location.objects.create(name="Main Location", organization=org)
```

---

## 🎯 Next Steps

1. ✅ Access admin panel and configure initial data
2. ✅ Test API endpoints via Swagger UI
3. ✅ Verify frontend-backend communication
4. ✅ Test booking flow
5. ✅ Set up periodic tasks in Celery Beat

---

**Ready to launch!** Choose your path above and follow the steps. 🚀

