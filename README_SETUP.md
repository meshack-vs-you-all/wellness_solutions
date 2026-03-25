# 🚀 Quick Setup Reference

**For:** Developers setting up Wellness Solutions locally  
**Time:** ~10 minutes

---

## ⚡ Fastest Path to Running

### 1. Create Frontend Environment File

```bash
cd frontend
cat > .env.local << 'EOF'
VITE_API_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000
EOF
cd ..
```

### 2. Resolve Port Conflicts

**Option A: Use Existing Services (Recommended)**

Update `.envs/.local/.postgres`:
```bash
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5432
POSTGRES_DB=wellness_solutions
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-actual-password
DATABASE_URL=postgres://postgres:your-actual-password@host.docker.internal:5432/wellness_solutions
```

Update `.envs/.local/.django`:
```bash
REDIS_URL=redis://host.docker.internal:6379/1
EMAIL_HOST=host.docker.internal
```

Then start only Django services:
```bash
docker-compose -f docker-compose.local.yml up django celeryworker celerybeat flower --build -d
```

**Option B: Use Different Ports**

```bash
cp docker-compose.local.override.yml.example docker-compose.local.override.yml
docker-compose -f docker-compose.local.yml -f docker-compose.local.override.yml up --build -d
```

### 3. Initialize Database

```bash
docker-compose -f docker-compose.local.yml exec django python manage.py migrate
docker-compose -f docker-compose.local.yml exec django python manage.py createsuperuser
```

### 4. Start Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

### 5. Access

- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/api/docs/

---

## 📚 Full Documentation

- **[RUN_EVERYTHING_NOW.md](./RUN_EVERYTHING_NOW.md)** - Complete launch guide
- **[PORT_SAFETY_MATRIX.md](./PORT_SAFETY_MATRIX.md)** - Port conflict solutions
- **[LOCAL_ACCESS_MAP.md](./LOCAL_ACCESS_MAP.md)** - All endpoints
- **[VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md)** - Full verification

---

**That's it!** 🎉

