# Quick Start Guide - Wellness Solutions

## 🚀 Fastest Way to Get Running

### Prerequisites Check

```bash
# Check Docker
docker --version
docker-compose --version

# Check Node.js (for frontend)
node --version  # Should be 20+
pnpm --version  # or npm --version
```

### Step 1: Environment Setup ✅ (Already Created)

Environment files have been created in `.envs/.local/`:
- `.envs/.local/.django` - Django settings
- `.envs/.local/.postgres` - Database settings

### Step 2: Handle Port Conflicts

**Current Situation:**
- Port 5432 (PostgreSQL) - Used by existing `postgres` container
- Port 6379 (Redis) - Used by existing `redis` container
- Port 8025/1025 (Mailpit) - Used by existing `mailpit` container
- Port 8000 (Django) - ✅ Available
- Port 5173 (Frontend) - ✅ Available

**Solution:** The Docker Compose file is configured to use internal service names. If you want to use existing services, you'll need to modify the compose file or use the existing containers.

### Step 3: Start the Application

#### Option A: Full Docker Setup (Recommended)

```bash
# Build and start all services
docker-compose -f docker-compose.local.yml up --build -d

# Run migrations
docker-compose -f docker-compose.local.yml exec django python manage.py migrate

# Create superuser
docker-compose -f docker-compose.local.yml exec django python manage.py createsuperuser

# View logs
docker-compose -f docker-compose.local.yml logs -f django
```

#### Option B: Use Existing Services

If you want to use your existing PostgreSQL and Redis containers:

1. **Modify `.envs/.local/.postgres`:**
   ```bash
   POSTGRES_HOST=host.docker.internal  # or your Docker host IP
   POSTGRES_PORT=5432
   POSTGRES_DB=wellness_solutions
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your-existing-postgres-password
   DATABASE_URL=postgres://postgres:your-existing-postgres-password@host.docker.internal:5432/wellness_solutions
   ```

2. **Modify `.envs/.local/.django`:**
   ```bash
   REDIS_URL=redis://host.docker.internal:6379/1
   ```

3. **Update `docker-compose.local.yml`** to remove postgres and redis services, or comment them out.

### Step 4: Start Frontend

```bash
cd frontend
pnpm install  # or npm install
pnpm dev      # or npm run dev
```

### Step 5: Access the Application

- **Backend:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **API Docs:** http://localhost:8000/api/docs
- **Frontend:** http://localhost:5173
- **Mailpit:** http://localhost:8025 (if using Docker mailpit)
- **Flower:** http://localhost:5555 (if Celery is running)

### Troubleshooting

#### Database Connection Issues

```bash
# Test PostgreSQL connection
docker-compose -f docker-compose.local.yml exec django python manage.py dbshell

# Or if using existing postgres
psql -h localhost -U postgres -d wellness_solutions
```

#### Redis Connection Issues

```bash
# Test Redis connection
docker-compose -f docker-compose.local.yml exec django python -c "import redis; r = redis.from_url('redis://redis:6379/1'); print(r.ping())"
```

#### Port Already in Use

If port 8000 is in use:
```bash
# Find what's using the port
lsof -i :8000
# or
ss -tlnp | grep :8000

# Change port in docker-compose.local.yml
# Update: "8008:8000" instead of "8000:8000"
```

#### Missing Dependencies

```bash
# Rebuild Docker images
docker-compose -f docker-compose.local.yml build --no-cache

# Or install locally
pip install -r requirements/local.txt
```

### Next Steps

1. ✅ Create a superuser account
2. ✅ Access admin panel and configure initial data
3. ✅ Test API endpoints
4. ✅ Verify frontend-backend integration
5. ✅ Set up Celery workers for background tasks

### Useful Commands

```bash
# View all logs
docker-compose -f docker-compose.local.yml logs -f

# Restart a service
docker-compose -f docker-compose.local.yml restart django

# Stop all services
docker-compose -f docker-compose.local.yml down

# Stop and remove volumes (⚠️ deletes data)
docker-compose -f docker-compose.local.yml down -v

# Run Django shell
docker-compose -f docker-compose.local.yml exec django python manage.py shell_plus

# Run tests
docker-compose -f docker-compose.local.yml exec django pytest
```

---

**For detailed information, see [AUDIT_REPORT.md](./AUDIT_REPORT.md)**

