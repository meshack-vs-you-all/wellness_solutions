# 🔌 Port Safety Matrix

**Last Updated:** 2024-12-19  
**System:** WSL2 Linux  
**Purpose:** Identify port conflicts and safe alternatives

---

## 📊 Current Port Status

| Port | Service | Current Usage | Conflict? | Safe Alternative | Action Required |
|------|---------|--------------|-----------|-----------------|-----------------|
| **80** | HTTP | traefik | ❌ No | N/A | Not used |
| **443** | HTTPS | traefik | ❌ No | N/A | Not used |
| **1025** | SMTP | mailpit | 🟡 **SHARED** | 1026 | Can share or use 1026 |
| **3000** | Web UI | open-webui | ❌ No | N/A | Not used by project |
| **5173** | Frontend | **AVAILABLE** | ✅ **SAFE** | N/A | **✅ USE THIS** |
| **5432** | PostgreSQL | postgres, ihatemoney-db | 🔴 **CONFLICT** | 5433 | **⚠️ MUST RESOLVE** |
| **5555** | Flower | **AVAILABLE** | ✅ **SAFE** | N/A | **✅ USE THIS** |
| **5678** | n8n | n8n | ❌ No | N/A | Not used by project |
| **6379** | Redis | redis | 🔴 **CONFLICT** | 6380 | **⚠️ MUST RESOLVE** |
| **8000** | Django | ihatemoney (internal) | ✅ **SAFE*** | 8008 | **✅ USE THIS** |
| **8025** | Mailpit UI | mailpit | 🟡 **SHARED** | 8026 | Can share or use 8026 |
| **9000-9001** | Minio | minio | ❌ No | N/A | Not used by project |

**Legend:**
- ✅ **SAFE** - Port is available and safe to use
- 🔴 **CONFLICT** - Port is in use, must resolve
- 🟡 **SHARED** - Port is in use but can be shared
- ⚠️ **MUST RESOLVE** - Critical conflict that prevents startup
- ❌ **No** - Not used by this project

**Note:** Port 8000 shows `ihatemoney` but it's only internal (not exposed to host), so it's safe.

---

## 🔴 Critical Conflicts

### 1. PostgreSQL (Port 5432)

**Current Status:**
- `postgres` container using port 5432
- `ihatemoney-db` container using port 5432 (internal)

**Impact:** 🔴 **CRITICAL** - Docker Compose will fail to start new postgres container

**Solutions:**

#### Option A: Use Existing PostgreSQL (Recommended)
```yaml
# In docker-compose.local.yml, comment out postgres service
# Or use external service configuration
```

**Environment Update:**
```bash
# .envs/.local/.postgres
POSTGRES_HOST=host.docker.internal  # or your Docker host IP
POSTGRES_PORT=5432
POSTGRES_DB=wellness_solutions
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-existing-password
DATABASE_URL=postgres://postgres:your-existing-password@host.docker.internal:5432/wellness_solutions
```

#### Option B: Use Different Port
```yaml
# docker-compose.local.yml or override
services:
  postgres:
    ports:
      - "5433:5432"  # Host port 5433, container port 5432
```

**No environment changes needed** (internal port stays 5432)

#### Option C: Use Different Database Name
If using existing postgres, just use a different database name:
```bash
POSTGRES_DB=wellness_solutions  # Different from ihatemoney's database
```

---

### 2. Redis (Port 6379)

**Current Status:**
- `redis` container using port 6379

**Impact:** 🔴 **CRITICAL** - Docker Compose will fail to start new redis container

**Solutions:**

#### Option A: Use Existing Redis (Recommended)
```bash
# .envs/.local/.django
REDIS_URL=redis://host.docker.internal:6379/1  # Use DB 1 instead of 0
```

**Note:** Using database 1 to avoid conflicts with other services using DB 0

#### Option B: Use Different Port
```yaml
# docker-compose.local.yml or override
services:
  redis:
    ports:
      - "6380:6379"  # Host port 6380, container port 6379
```

**Environment Update:**
```bash
# .envs/.local/.django
REDIS_URL=redis://redis:6379/1  # Internal name stays redis, port stays 6379
```

---

## 🟡 Shared Ports (Can Share)

### 1. Mailpit (Ports 8025, 1025)

**Current Status:**
- `mailpit` container using ports 8025 (UI) and 1025 (SMTP)

**Impact:** 🟡 **LOW** - Can share the same mailpit instance

**Solutions:**

#### Option A: Share Existing Mailpit (Recommended)
```bash
# .envs/.local/.django
EMAIL_HOST=host.docker.internal
EMAIL_PORT=1025
```

**Remove mailpit service from docker-compose.local.yml or comment it out**

#### Option B: Use Different Ports
```yaml
services:
  mailpit:
    ports:
      - "8026:8025"  # UI on 8026
      - "1026:1025"  # SMTP on 1026
```

**Update environment:**
```bash
EMAIL_PORT=1026
```

---

## ✅ Safe Ports (No Conflicts)

### Port 8000 - Django
- **Status:** ✅ **SAFE**
- **Current:** `ihatemoney` uses it internally but not exposed
- **Action:** Use as-is

### Port 5173 - Frontend (Vite)
- **Status:** ✅ **SAFE**
- **Current:** Available
- **Action:** Use as-is

### Port 5555 - Flower
- **Status:** ✅ **SAFE**
- **Current:** Available
- **Action:** Use as-is

---

## 🔧 Recommended Configuration

### For Your Current Setup (Existing Services)

**Recommended Approach:** Use existing postgres, redis, and mailpit

**Configuration:**

1. **Update `.envs/.local/.postgres`:**
```bash
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5432
POSTGRES_DB=wellness_solutions
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-existing-password
DATABASE_URL=postgres://postgres:your-existing-password@host.docker.internal:5432/wellness_solutions
```

2. **Update `.envs/.local/.django`:**
```bash
REDIS_URL=redis://host.docker.internal:6379/1
EMAIL_HOST=host.docker.internal
EMAIL_PORT=1025
```

3. **Modify `docker-compose.local.yml`:**
   - Comment out `postgres` service
   - Comment out `redis` service
   - Comment out `mailpit` service
   - Remove them from `depends_on` in django service

4. **Start only Django and Celery:**
```bash
docker-compose -f docker-compose.local.yml up django celeryworker celerybeat flower --build -d
```

---

## 🧪 Port Conflict Testing

### Test if Port is Available

```bash
# Check if port is in use
ss -tlnp | grep :8000
# or
lsof -i :8000
# or
netstat -tlnp | grep :8000
```

### Test Port from Container

```bash
# Test if host service is accessible from container
docker-compose -f docker-compose.local.yml exec django ping host.docker.internal
docker-compose -f docker-compose.local.yml exec django nc -zv host.docker.internal 5432
docker-compose -f docker-compose.local.yml exec django nc -zv host.docker.internal 6379
```

---

## 📋 Port Allocation Summary

### Project Ports (After Resolution)

| Service | Internal Port | Host Port | Status |
|---------|---------------|-----------|--------|
| Django | 8000 | 8000 | ✅ Safe |
| Frontend | 5173 | 5173 | ✅ Safe |
| Flower | 5555 | 5555 | ✅ Safe |
| PostgreSQL | 5432 | 5432* | ⚠️ Use existing |
| Redis | 6379 | 6379* | ⚠️ Use existing |
| Mailpit UI | 8025 | 8025* | 🟡 Share existing |
| Mailpit SMTP | 1025 | 1025* | 🟡 Share existing |

*If using existing services, these are accessed via `host.docker.internal`

### Alternative Ports (If Needed)

| Service | Alternative Host Port | Internal Port |
|---------|----------------------|---------------|
| PostgreSQL | 5433 | 5432 |
| Redis | 6380 | 6379 |
| Mailpit UI | 8026 | 8025 |
| Mailpit SMTP | 1026 | 1025 |
| Django | 8008 | 8000 |

---

## 🚨 Conflict Resolution Checklist

- [ ] Identify which services you want to use (existing vs new)
- [ ] Update environment files accordingly
- [ ] Modify docker-compose.yml if needed
- [ ] Test port connectivity
- [ ] Verify services start without errors
- [ ] Document your chosen configuration

---

## 📝 Notes

1. **WSL2 Networking:** `host.docker.internal` should work, but if not, use your WSL IP:
   ```bash
   hostname -I | awk '{print $1}'
   ```

2. **Docker Networks:** Services in same docker-compose file share a network automatically

3. **Port Mapping:** Format is `HOST:CONTAINER` - internal port can stay the same

4. **Database Isolation:** Using different database names allows sharing same PostgreSQL instance

5. **Redis Databases:** Redis supports multiple databases (0-15), use DB 1 for isolation

---

**All conflicts identified and solutions provided!** ✅

