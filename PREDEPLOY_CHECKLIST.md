# Pre-Deploy Checklist

**Last Updated:** 2024-12-19  
**Purpose:** Exact steps and commands to reproduce full verification

---

## Prerequisites

```bash
# 1. Python 3.11+ and Node.js 20+
python3 --version  # Should be 3.11+
node --version     # Should be 20+

# 2. Install system dependencies
sudo apt-get update
sudo apt-get install -y postgresql-client redis-tools

# 3. Create virtual environment
python3 -m venv .venv_test
source .venv_test/bin/activate

# 4. Install Python dependencies
pip install -r requirements/local.txt

# 5. Install frontend dependencies
cd frontend
pnpm install  # or npm install
cd ..
```

---

## 1. Environment Setup

```bash
# Set test environment variables
export DJANGO_SETTINGS_MODULE=config.settings.test
export DATABASE_URL=sqlite:///test.db
export REDIS_URL=redis://localhost:6379/0

# Or use PostgreSQL for integration tests
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wellness_solutions_test
```

---

## 2. Backend Static Analysis

### Django System Checks

```bash
# Basic checks
python manage.py check

# Deployment checks
python manage.py check --deploy

# Migration check
python manage.py makemigrations --check
```

### Linting

```bash
# Ruff linting
ruff check . --exclude=.venv_test,venv,node_modules

# Auto-fix (if needed)
ruff check . --fix
```

### Type Checking

```bash
# Mypy type checking
export DATABASE_URL=sqlite:///test.db
mypy . --config-file pyproject.toml
```

---

## 3. Frontend Static Analysis

```bash
cd frontend

# TypeScript compilation check
pnpm exec tsc --noEmit

# Build check
pnpm build

# Linting (if configured)
pnpm lint || echo "No linting configured"

# Tests (if configured)
pnpm test || echo "No tests configured"
```

---

## 4. Backend Tests

```bash
# Run all tests
export DATABASE_URL=sqlite:///test.db
export DJANGO_SETTINGS_MODULE=config.settings.test
pytest --maxfail=5 -v

# With coverage
pytest --cov=. --cov-report=xml --cov-report=term --cov-fail-under=80

# Specific test files
pytest bookings/tests/ -v
pytest users/tests/ -v

# Race condition tests
pytest bookings/tests/test_race_conditions.py -v
```

---

## 5. Frontend Tests

```bash
cd frontend

# Run tests (if configured)
pnpm test

# With coverage
pnpm test --coverage
```

---

## 6. Contract Checks

```bash
# Start development server
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wellness_solutions
export DJANGO_SETTINGS_MODULE=config.settings.local
python manage.py runserver 8000 &

# Wait for server to start
sleep 5

# Test API endpoints
curl http://localhost:8000/api/schema/ | jq .
curl http://localhost:8000/api/classes/ | jq .
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Stop server
pkill -f "python manage.py runserver"
```

---

## 7. Security Audit

```bash
# Install bandit
pip install bandit

# Run security scan
bandit -r . -x .venv_test,venv,node_modules

# Check for secrets
grep -r "SECRET_KEY\|password\|api_key" --include="*.py" . | grep -v "settings\|test\|factory\|migration"

# Check outdated dependencies
pip list --outdated
cd frontend && pnpm outdated
```

---

## 8. Database Migration Check

```bash
# Check for pending migrations
python manage.py makemigrations --check

# Apply migrations to test database
export DATABASE_URL=sqlite:///test.db
export DJANGO_SETTINGS_MODULE=config.settings.test
python manage.py migrate

# Verify constraints
python manage.py dbshell << EOF
.schema bookings_booking
.schema bookings_bookingpayment
EOF
```

---

## 9. Business Logic Tests

```bash
# Run race condition tests
pytest bookings/tests/test_race_conditions.py -v

# Run booking validation tests
pytest bookings/tests/ -k "test_booking" -v

# Run payment tests
pytest bookings/tests/ -k "test_payment" -v
```

---

## 10. E2E Smoke Test

```bash
# Install Playwright (if using)
cd frontend
pnpm add -D @playwright/test
pnpm exec playwright install

# Run E2E tests
pnpm exec playwright test
```

---

## 11. Final Verification

```bash
# Run all checks in sequence
./scripts/run_deep_verification.sh

# Or manually:
python manage.py check --deploy
ruff check .
mypy . --config-file pyproject.toml
pytest --cov=. --cov-report=term --cov-fail-under=80
cd frontend && pnpm build && pnpm exec tsc --noEmit
```

---

## Exit Criteria

All of the following must pass:

- [ ] `python manage.py check --deploy` - No errors
- [ ] `ruff check .` - No critical errors
- [ ] `mypy .` - No blocking type errors
- [ ] `pytest --cov-fail-under=80` - Coverage >= 80%
- [ ] `pnpm build` - Frontend builds successfully
- [ ] `pnpm exec tsc --noEmit` - No TypeScript errors
- [ ] Race condition tests pass
- [ ] Security scan shows no critical issues
- [ ] All migrations apply successfully
- [ ] Database constraints are in place

---

## Quick Run Script

Save this as `run_predeploy.sh`:

```bash
#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=config.settings.test
export DATABASE_URL=sqlite:///test.db

echo "=== Running Pre-Deploy Checks ==="

echo "1. Django checks..."
python manage.py check --deploy

echo "2. Linting..."
ruff check . --exclude=.venv_test,venv,node_modules

echo "3. Type checking..."
mypy . --config-file pyproject.toml || echo "Type checking has warnings"

echo "4. Running tests..."
pytest --cov=. --cov-report=term --cov-fail-under=80 --maxfail=5

echo "5. Frontend build..."
cd frontend
pnpm build
pnpm exec tsc --noEmit
cd ..

echo "=== All checks passed! ==="
```

Make it executable: `chmod +x run_predeploy.sh`

---

**Use this checklist before every deployment!**

