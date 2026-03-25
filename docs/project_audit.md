## Project Audit — Wellness Solutions

### High-Level Description

Wellness Solutions is a full-stack booking, payments, and user-management platform for a stretching and fitness studio. It provides scheduling and booking of sessions, management of instructors and locations, corporate service programmes, and payment/package handling, exposed through both a web UI and a REST API.

### Architecture Overview

- **Backend**
  - Django 5.0 application (`config` + multiple domain apps such as `users`, `bookings`, `services`, `locations`, `wellness_instructors`, `clients`, `schedules`, `packages`).
  - Django REST Framework for a JSON API (documented with drf-spectacular/OpenAPI).
  - Celery + Redis for background jobs and periodic tasks.
  - PostgreSQL as the primary database.
  - Tailwind CSS + Django templates for server-rendered pages (via `theme` app and `django-tailwind`).
  - Sphinx documentation under `docs/` with detailed guides (`quickstart`, `architecture`, `deployment`, `roadmap`, etc.).

- **Frontend**
  - Separate React SPA in `frontend/` using Vite 6.
  - React 19, React Router, React Hook Form, Recharts, Lucide icons.
  - Tailwind CSS 4 via PostCSS.

- **Infrastructure & Tooling**
  - Docker-based local and production images under `compose/local` and `compose/production`.
  - GitHub Actions workflow `.github/workflows/predeploy.yml` running tests, linting, type checks, coverage, and security scans.
  - Sentry integration for error tracking.
  - Sendgrid via django-anymail for outbound email (production).

### Major Components

- **Backend services**
  - `users`: custom user model (email-based login, extended profile, organization links).
  - `bookings`: rich booking model with types, statuses, payment status, pricing, validation, and metadata.
  - `services`: organization and service management (proposals, corporate programmes, etc. per docs).
  - `locations`: location, instructor, and service relationships.
  - `wellness_instructors`: instructor profiles and availability.
  - `schedules`: calendar and schedule management.
  - `packages`: package/subscription support used by bookings.
  - `clients`: client-related domain logic.
  - `docs`: Sphinx-powered documentation site.

- **Frontend**
  - `frontend/` React + Vite app for a modern UI on top of the API.
  - Uses Vite dev server on port 5173 (`vite.config.ts`) and Vite `VITE_`-prefixed env vars.

- **Background processing**
  - Celery workers and beat scheduler configured against Redis (`REDIS_URL`).
  - Flower support for monitoring Celery in local Docker.

- **Documentation**
  - Sphinx docs in `docs/`:
    - `quickstart.rst`: local dev setup (Python, Postgres, Redis, Node) and project structure.
    - `architecture.rst`: layered architecture, core models, and API design.
    - `deployment.rst`: multi-env AWS/Kubernetes deployment strategy.
    - `roadmap.rst`: phased roadmap and technical milestones.

### Dependencies

- **Python / Django**
  - Django 5.0.9
  - django-environ, django-model-utils
  - django-allauth (with MFA) for auth and social login
  - djangorestframework
  - django-cors-headers
  - drf-spectacular for API docs
  - Celery 5.4.0, django-celery-beat, flower
  - redis / hiredis, django-redis, django-cacheops
  - whitenoise for static files
  - Pillow, python-slugify
  - django-crispy-forms + crispy-tailwind
  - django-ratelimit, bleach (security)

- **Tooling & quality**
  - pytest, pytest-django, coverage, django-coverage-plugin
  - mypy with django- and DRF-stubs (configured via `pyproject.toml`)
  - ruff (lint/format), djlint (templates)
  - factory-boy, django-extensions, django-debug-toolbar, django-browser-reload
  - Sphinx + sphinx-autobuild + sphinx-rtd-theme

- **Production**
  - gunicorn
  - psycopg 3 (binary extras)
  - sentry-sdk
  - django-anymail[sendgrid]

- **Frontend**
  - React 19, React DOM
  - React Router DOM
  - React Hook Form
  - Axios
  - Recharts
  - Lucide React
  - Vite, TypeScript, Tailwind CSS, PostCSS, autoprefixer

### Required Environment Variables

Based on `config/settings/base.py`, `config/settings/local.py`, and `config/settings/production.py`:

- **Core / shared**
  - **`DATABASE_URL`**: PostgreSQL DSN. Used by `env.db("DATABASE_URL")` to configure `DATABASES["default"]`.
  - **`REDIS_URL`**: Redis DSN (default `redis://redis:6379/0` in base, overridden as needed). Used for:
    - Celery broker and result backend.
    - Django cache backend in base/production.
  - **`DJANGO_READ_DOT_ENV_FILE`**: When `True`, `.env` at project root is read by django-environ.
  - **`DJANGO_DEBUG`**: Boolean flag for debug mode (default `False` in base, overridden to `True` in `local.py`).

- **Local / development (config.settings.local)**
  - **`DJANGO_SECRET_KEY`**: Secret key (a default development value is provided but should be overridden locally).
  - **`EMAIL_HOST`**: Defaults to `mailpit` for local email capture.
  - **`USE_DOCKER`**: When set to `"yes"`, used to compute `INTERNAL_IPS` for debug toolbar.

- **Production (config.settings.production)**
  - **`DJANGO_SECRET_KEY`**: Required, no default.
  - **`DJANGO_ALLOWED_HOSTS`**: Comma-separated list of hosts (parsed via `env.list`, default `["jpfwellnesssolutions.com"]`).
  - **`CONN_MAX_AGE`**: DB connection lifetime (seconds, default 60).
  - **`DJANGO_SECURE_SSL_REDIRECT`**: Enables HTTPS redirect (default `True`).
  - **`DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`**
  - **`DJANGO_SECURE_HSTS_PRELOAD`**
  - **`DJANGO_SECURE_CONTENT_TYPE_NOSNIFF`**
  - **`DJANGO_DEFAULT_FROM_EMAIL`**
  - **`DJANGO_SERVER_EMAIL`**
  - **`DJANGO_EMAIL_SUBJECT_PREFIX`**
  - **`DJANGO_ADMIN_URL`**: Custom admin URL path.
  - **`SENDGRID_API_KEY`**, **`SENDGRID_API_URL`**: For django-anymail/Sendgrid.
  - **`COMPRESS_ENABLED`**: Controls django-compressor in production (default `True`).
  - **`SENTRY_DSN`**
  - **`DJANGO_SENTRY_LOG_LEVEL`**
  - **`SENTRY_ENVIRONMENT`**
  - **`SENTRY_TRACES_SAMPLE_RATE`**

- **Other application settings (base)**
  - **`DJANGO_EMAIL_BACKEND`** (optional override of email backend).
  - **`DJANGO_DEFAULT_FROM_EMAIL`**, **`DJANGO_SERVER_EMAIL`** (overridable defaults).
  - **`DJANGO_SITE_NAME`**, **`DJANGO_SITE_URL`**: Branding and canonical URL.
  - **`DJANGO_ADMIN_FORCE_ALLAUTH`**: Forces admin sign-in through allauth.
  - **`DJANGO_ACCOUNT_ALLOW_REGISTRATION`**: Controls self-service signups.

> **Note**: Local `.env` usage requires setting `DJANGO_READ_DOT_ENV_FILE=True` or exporting environment variables directly, which is not explicitly called out in existing quickstart docs.

### External Services and APIs

- **PostgreSQL**: Primary relational database (local: `localhost:5432`, CI uses ephemeral `postgres:15` service).
- **Redis**: Caching, Celery broker, and session cache (local: `localhost:6379`, CI uses `redis:6` service).
- **Sendgrid**: Email delivery in production via django-anymail.
- **Sentry**: Error tracking and performance telemetry.
- **Mailpit**: Local SMTP debugging server (Docker-based).
- **AWS (per `deployment.rst`)**:
  - EC2 for app servers.
  - RDS for PostgreSQL.
  - ElastiCache for Redis.
  - S3 + CloudFront for static/media and CDN.
  - Route 53, VPC, ELB.

### Missing or Unclear Documentation

- **Local `.env` behaviour**: Quickstart describes creating `.env` with `DATABASE_URL` and `REDIS_URL` but does not mention enabling `DJANGO_READ_DOT_ENV_FILE` or exporting vars in the shell. This could confuse new contributors.
- **React/Vite frontend**:
  - No dedicated markdown/Sphinx page documenting the frontend structure, environment variables (e.g. API base URL), and how it connects to the Django API.
  - No documented local workflow for running Django and Vite together (ports, CORS, auth story).
- **Docker / Docker Compose**:
  - Dockerfiles exist under `compose/`, but there is no obvious `local.yml`/`docker-compose.yml` at the project root, and no markdown tying together the container topology and commands.
- **Demo data / seeding**:
  - Roadmap mentions initial fixtures and sample data, but concrete fixture file names and loading instructions are not documented.
- **Monitoring/logging stack**:
  - Sentry is documented at a high level, but there is no environment-specific runbook for logs, error triage, and alerting beyond Sentry configuration.

### Recent Development Activity

Because the current workspace is not recognised as a git repository by this environment, and shell/git commands are not executable here, this section is based on static inspection of the codebase and documentation rather than commit history.

- **Recent features and areas that appear most recently worked on**
  - **Modern React frontend**:
    - New `frontend/` Vite + React 19 app with TypeScript and Tailwind 4.
    - CI pipeline (`predeploy.yml`) explicitly builds and tests this frontend, indicating it is a first-class, actively maintained component.
  - **Pre-deploy CI pipeline**:
    - GitHub Actions workflow running:
      - Python dependency install from `requirements/local.txt`.
      - Django system checks, migration checks, migrations, pytest with coverage.
      - Ruff and mypy.
      - pnpm-based frontend build and tests.
      - Bandit and a simple secret scan.
    - Suggests recent focus on tightening quality gates before deployment.
  - **Advanced booking & domain models**:
    - Rich `bookings` model (multiple statuses, relationships to locations, services, instructors, packages, and detailed validation hooks).
    - Extended `users.User` model with organization and profile metadata.
    - Roadmap marks the service management module as complete and the advanced booking system as in progress.

- **Work-in-progress / partially implemented features (from `docs/roadmap.rst` and code)**
  - **Advanced Booking System**:
    - Features like real-time availability, waitlists, iCal integration, and WebSocket notifications are documented as in-progress, but their implementation completeness is not verifiable without running the app and tests.
  - **Payment and Subscription Platform**:
    - Roadmap shows this as in progress; payment models, gateways, billing flows, and reconciliation need focused end-to-end testing.
  - **Responsive UI and dashboards**:
    - Base templates, layouts, and authentication flows are marked as completed; interactive calendar, admin dashboards, and full mobile optimizations are still marked as pending.
  - **DevOps & observability**:
    - Development environment, CI/CD, and containerization are marked complete.
    - Monitoring, logging, backup/recovery procedures, and full production hardening are still listed as TODO.

- **Potentially fragile or incomplete areas**
  - **Real-time and external integrations**:
    - WebSocket-based updates, calendar sync, and payment gateways are complex and listed as in-progress; these are likely sources of bugs until thoroughly tested.
  - **Configuration consistency**:
    - Discrepancy between `.env` expectations in docs and actual settings (`DJANGO_READ_DOT_ENV_FILE`) could cause local setup issues.
    - Multiple storage strategies are described in docs (AWS S3) vs. current `STORAGES` configuration (local filesystem + Whitenoise) and should be reconciled for production.
  - **Test status**:
    - The codebase is wired for robust testing (pytest, coverage, mypy, ruff), but tests were not executed in this environment due to shell limitations, so current pass/fail status is unknown.

