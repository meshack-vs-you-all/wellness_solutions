## Deployment Readiness Assessment

This document assesses how ready Wellness Solutions is for deployment to cloud platforms (AWS, Railway, Render, Fly.io, etc.) and outlines recommended commands and configuration.

> **Note**: In this environment I cannot run deployments, Docker images, or CI pipelines directly. The assessment below is based on static analysis of the repository (`config/settings/*`, `requirements/*`, `.github/workflows/predeploy.yml`, and Sphinx docs), not on a live deployment.

---

### 1. Overall Readiness Level

- **Status**: **Partially ready for production deployment**

**Strengths**

- Production-specific Django settings (`config/settings/production.py`) with:
  - Strict security settings (HSTS, secure cookies, SSL redirect, secure headers).
  - Redis-backed caching via `django-redis`.
  - Sentry error reporting and logging integration.
  - AnyMail/Sendgrid configuration for email.
  - Staticfiles storage via Whitenoise compressed manifest storage.
- Clear environment-specific docs in `docs/deployment.rst` describing AWS-based infrastructure.
- CI pipeline (`.github/workflows/predeploy.yml`) that:
  - Spins up Postgres and Redis services.
  - Installs dependencies from `requirements/local.txt`.
  - Runs Django checks, migration checks, migrations.
  - Runs Ruff, mypy, and pytest with coverage gate.
  - Builds and tests the Vite/React frontend.
  - Runs basic security scans (bandit, simple secret grep).
- Dockerfiles for Django (local and production modes) with multi-stage builds and Node/Tailwind tooling.

**Gaps / Risks**

- No top-level `docker-compose.yml` or `local.yml` committed for orchestrating all services (web, worker, beat, Redis, Postgres, Mailpit, docs) in one command; docs refer to `docker-compose.local.yml` which is not present here.
- Deployment docs focus on AWS + Kubernetes; there is no provider-specific recipe for Railway/Render/Fly.io.
- Some advanced features listed in the roadmap (full payment gateway integration, WebSocket notifications, advanced booking flows) are documented as in-progress; their production readiness depends on test coverage and live testing.

---

### 2. Required Environment Variables (Production)

From `config/settings/base.py` and `config/settings/production.py`:

- **Core**
  - `DATABASE_URL` — PostgreSQL DSN (e.g. `postgresql://user:pass@host:5432/dbname`).
  - `REDIS_URL` — Redis DSN (e.g. `redis://host:6379/0`).
  - `DJANGO_SECRET_KEY` — cryptographically strong secret key.
  - `DJANGO_ALLOWED_HOSTS` — comma-separated list of allowed hostnames.
  - `CONN_MAX_AGE` — optional DB connection lifetime in seconds (default: 60).

- **Security / HTTPS**
  - `DJANGO_SECURE_SSL_REDIRECT` (default `True`).
  - `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` (default `True`).
  - `DJANGO_SECURE_HSTS_PRELOAD` (default `True`).
  - `DJANGO_SECURE_CONTENT_TYPE_NOSNIFF` (default `True`).

- **Email**
  - `DJANGO_DEFAULT_FROM_EMAIL` (default `Wellness Solutions <noreply@jpfwellnesssolutions.com>`).
  - `DJANGO_SERVER_EMAIL` (defaults to `DJANGO_DEFAULT_FROM_EMAIL`).
  - `DJANGO_EMAIL_SUBJECT_PREFIX` (default `[Wellness Solutions] `).

- **Admin**
  - `DJANGO_ADMIN_URL` — path segment for admin (e.g. `secret-admin/`).

- **Sendgrid (AnyMail)**
  - `SENDGRID_API_KEY`
  - `SENDGRID_API_URL` (default `https://api.sendgrid.com/v3/`)

- **Sentry**
  - `SENTRY_DSN`
  - `DJANGO_SENTRY_LOG_LEVEL` (default `INFO`).
  - `SENTRY_ENVIRONMENT` (e.g. `production`, `staging`).
  - `SENTRY_TRACES_SAMPLE_RATE` (e.g. `0.1`).

- **Misc / base**
  - `DJANGO_EMAIL_BACKEND` (optional override).
  - `DJANGO_DEFAULT_FROM_EMAIL`, `DJANGO_SERVER_EMAIL` (overrides).
  - `DJANGO_SITE_NAME`, `DJANGO_SITE_URL`.
  - `DJANGO_ADMIN_FORCE_ALLAUTH`.
  - `DJANGO_ACCOUNT_ALLOW_REGISTRATION`.

All of these should be configured in the target hosting provider’s environment variable system or via a secrets manager.

---

### 3. Build & Run Commands (Backend)

For a typical production container (non-Docker-orchestrated platform, e.g. Railway/Render/Fly.io):

- **Python version**: `3.11`
- **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements/production.txt
```

- **Collect static files**

```bash
python manage.py collectstatic --noinput
```

- **Run migrations**

```bash
python manage.py migrate --noinput
```

- **Start application (Gunicorn)**

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
```

Adjust worker count based on CPU and memory.

---

### 4. Containerization Status

- **Dockerfiles**
  - `compose/local/django/Dockerfile`:
    - Multi-stage build (wheels in `python-build-stage`, runtime in `python-run-stage`).
    - Installs Node.js 20, global Tailwind/PostCSS tooling.
    - Creates non-root `devuser` with isolated npm prefix.
    - Copies app into `/app`, installs Python wheels, and uses `/entrypoint` + `/start` scripts.
    - Local start script runs:
      - `python manage.py migrate`
      - `python manage.py runserver_plus 0.0.0.0:8000`
  - Production Dockerfile(s) exist under `compose/production/` for web workers and celery processes (not exhaustively reviewed here but follow cookiecutter-django patterns).

- **Compose**
  - Docs (`docs/howto.rst`) reference `docker compose -f docker-compose.local.yml up docs` but that file is not present in this snapshot.
  - You may have a `docker-compose.local.yml` or `local.yml` in another branch or private repo; if not, you will need to create a compose file that ties together:
    - Web (Django)
    - Celery worker
    - Celery beat
    - Postgres
    - Redis
    - Mailpit
    - Docs (optional)

**Impact**: The project is close to container-ready, but you will likely need to write or restore a `docker-compose.yml` for full multi-service orchestration.

---

### 5. Logging & Monitoring

- **Logging**
  - Production logging in `config/settings/production.py`:
    - Root logger with `DEBUG` to console.
    - Separate loggers for `django.db.backends`, `sentry_sdk`, `django.security.DisallowedHost`.
  - Base settings define more granular file handlers for `core`, `users`, `bookings`, etc., but in production the simplified logging dict is used.

- **Monitoring**
  - Sentry SDK configured with Django, Celery, Redis integrations.
  - `SPECTACULAR_SETTINGS["SERVERS"]` updated with production URL `https://jpfwellnesssolutions.com`.

**Gaps**

- No committed configuration for metrics (Prometheus, CloudWatch, etc.) or log shipping beyond Sentry and stdout logs.
- Backup and restore procedures for database and media are described at a high level in `docs/deployment.rst`, but the concrete scripts/automation are not present in this snapshot.

---

### 6. Deployment Architecture Recommendation

#### A. Traditional Cloud Stack (AWS-like, per existing docs)

- **Web tier**
  - Auto-scaled EC2/Kubernetes pods running Django + Gunicorn behind a load balancer.
  - Whitenoise for static file serving, or static files offloaded to S3 + CloudFront.
- **Data tier**
  - PostgreSQL via RDS.
  - Redis via ElastiCache (used for caching and Celery broker).
- **Background workers**
  - Celery worker and Celery beat deployments with the same image but different command.
- **Support services**
  - Mailpit for lower environments; Sendgrid in production.
  - Sentry for error reporting.

#### B. Simpler PaaS (Railway/Render/Fly.io)

- **Backend (web) service**
  - Single service running the Django app (Gunicorn).
  - Connects to managed PostgreSQL and Redis add-ons.
  - Whitenoise handles static files; media can be stored locally (with backup strategy) or via S3-compatible storage.
- **Worker service**
  - Separate deployment using the same image but running `celery -A config.celery_app worker -l info`.
- **Beat service**
  - Another deployment running `celery -A config.celery_app beat`.
- **Frontend**
  - Either:
    - Built into the Django static files (pre-built assets copied under `static/`), or
    - Served as a separate static site or Node service (Vite build output) behind the same domain.

---

### 7. Railway-Specific Plan

The app can run on Railway using native builds (no Dockerfile required), but you can also use the existing Docker image if you prefer more control.

#### 7.1 Services Required

- **Web (Django)**
  - Primary HTTP service, exposed to the internet.
- **Worker (Celery)**
  - Background task processing (optional initially if you are not using async features).
- **Beat (Celery Beat)**
  - Periodic tasks (optional at first).
- **PostgreSQL**
  - Managed Railway Postgres add-on.
- **Redis**
  - Managed Railway Redis add-on.

You can start with just **Web + Postgres + Redis**, and add worker/beat as the async features go live.

#### 7.2 Environment Variables on Railway

For each Django-related service (web/worker/beat), configure:

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_SECRET_KEY=<generated-strong-secret>`
- `DJANGO_ALLOWED_HOSTS=<your-railway-domain>,<custom-domain>`
- `DATABASE_URL=<Railway Postgres URL>`
- `REDIS_URL=<Railway Redis URL>`
- `DJANGO_DEFAULT_FROM_EMAIL`, `DJANGO_SERVER_EMAIL`
- `DJANGO_ADMIN_URL=admin/` (or a hardened custom path)
- `SENTRY_DSN` (optional but recommended)
- `SENTRY_ENVIRONMENT=railway-production`
- `SENTRY_TRACES_SAMPLE_RATE=0.0` (or small sample like `0.1`)
- `SENDGRID_API_KEY` (if using Sendgrid)

#### 7.3 Build & Start Commands (Railway Native Build)

- **Build command**

```bash
pip install --upgrade pip
pip install -r requirements/production.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

- **Start command (web service)**

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT} --workers 3
```

- **Start command (Celery worker service)**

```bash
celery -A config.celery_app worker -l info
```

- **Start command (Celery beat service)**

```bash
celery -A config.celery_app beat -l info
```

#### 7.4 Using Docker on Railway (Optional)

If you prefer to use the existing Docker configuration:

- Add a `Dockerfile` at the root (or reference `compose/production/django/Dockerfile`) that:
  - Installs `requirements/production.txt`.
  - Copies the project.
  - Runs `collectstatic` in the image build.
  - Uses `gunicorn` as the default CMD.
- Configure Railway service to **build from Dockerfile** instead of using native build.

Given Railway’s strong support for Python + Postgres, the **native build approach is usually simpler**, unless you need the exact same image across multiple environments.

---

### 8. Blockers / Action Items Before Production

- **Compose file**:
  - Add or restore a `docker-compose.yml` (or `docker-compose.local.yml`) that matches the described Docker topology.
- **Secrets management**:
  - Ensure all production secrets (`DJANGO_SECRET_KEY`, `SENDGRID_API_KEY`, `SENTRY_DSN`, database passwords) are stored only in environment variables or a secret manager; do not commit to git.
- **End-to-end tests of critical flows**:
  - Bookings, payments, schedule management, and corporate services should have high-coverage tests and be exercised in a staging environment that mirrors production.
- **Static/media storage**:
  - Decide whether to:
    - Keep staticfiles on disk + Whitenoise, and
    - Store media files on disk, S3, or another object store.
  - Align actual settings with the documented architecture.

Addressing these items will move the project from **Partially ready** to **Ready** for robust production deployment.

