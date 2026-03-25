## Project Summary — Wellness Solutions

### What the Application Does

Wellness Solutions is a full-featured booking and management platform for a stretching and fitness studio. It supports:

- User registration, authentication (with optional MFA), and profile management.
- Management of organizations, locations, services, instructors, and schedules.
- Booking of individual, corporate, and group sessions, with validation of availability and constraints.
- Package/subscription management and payment tracking.
- A modern React-based frontend experience backed by a robust Django REST API and server-rendered pages.

---

### Tech Stack

- **Backend**
  - Python 3.11
  - Django 5.0
  - Django REST Framework
  - django-allauth (with MFA) for authentication and social login.
  - Celery + Redis for asynchronous and periodic tasks.
  - PostgreSQL for relational data.
  - Tailwind CSS + Django templates (via `theme` app and `django-tailwind`).
  - Sphinx documentation (`docs/`).

- **Frontend**
  - React 19 + React Router.
  - Vite 6 bundler.
  - TypeScript.
  - Tailwind CSS 4.
  - Supporting libraries: Axios, React Hook Form, Recharts, Lucide icons.

- **Tooling & CI**
  - pytest, pytest-django, coverage.
  - mypy with django- and DRF-stubs.
  - ruff (lint/format), djlint for templates.
  - GitHub Actions pre-deploy workflow for backend and frontend checks.
  - Dockerfiles for local and production images.

---

### Current Development Status

Based on `docs/roadmap.rst`, `docs/architecture.rst`, and the existing models/configuration:

- **Completed / Mature**
  - Core data model and database schema (users, organizations, locations, services, bookings, packages, etc.).
  - Authentication system with JWT, MFA support, and RBAC.
  - Service management module (organizations, proposals, corporate programmes).
  - Base templates, layouts, and authentication flows.
  - Development environment, CI/CD pipeline, containerization strategy.

- **In Progress**
  - Advanced booking features (real-time availability, waitlists, WebSocket notifications, calendar integrations).
  - Payment and subscription flows (multi-gateway support, invoicing, analytics).
  - Responsive UI enhancements (interactive calendar, admin dashboards, mobile optimisations).
  - Observability: monitoring, logging beyond Sentry, backup/recovery runbooks.

- **Experimental / Potentially Fragile**
  - Real-time features (WebSockets) and external integrations (payment gateways, external calendars) that are complex and not fully verifiable in this audit environment.

---

### What Works vs. What Is Unfinished

**What likely works (given code and docs)**

- User auth and account management (including admin).
- CRUD operations and API structure for core entities.
- Basic booking creation and validation paths.
- React/Vite frontend scaffold, routing, and dashboards.
- Local dev, testing, and CI flows as defined in the docs and GitHub Actions.

**What is unfinished or needs careful testing**

- End-to-end booking journeys under edge cases (conflicts, cancellations, corporate flows).
- Full payment lifecycle across all gateways.
- WebSocket-based live updates and calendar sync.
- Advanced analytics dashboards and business intelligence features.
- Production-grade monitoring, alerting, and backup workflows.

---

### How to Run Locally (with Hot Reload)

See `docs/local_setup.md` for detailed, copy-pasteable commands. In summary:

- **Backend**
  - Create and activate a Python 3.11 virtualenv.
  - `pip install -r requirements/local.txt`
  - Ensure Postgres and Redis are running (via Docker or local installs).
  - Configure `.env` with at least:
    - `DJANGO_READ_DOT_ENV_FILE=True`
    - `DJANGO_DEBUG=True`
    - `DJANGO_SECRET_KEY=...`
    - `DATABASE_URL=postgresql://...`
    - `REDIS_URL=redis://...`
  - Run migrations and create a superuser.
  - Start dev server with auto-reload:
    - `python manage.py runserver_plus 0.0.0.0:8000`

- **Theme / Tailwind**
  - `cd theme/static_src`
  - `pnpm install` (or `npm install`), then `pnpm run dev` to watch and rebuild CSS.

- **Frontend SPA**
  - `cd frontend`
  - `pnpm install` (or `npm install`)
  - Optionally set `VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1` in `frontend/.env.local`.
  - `pnpm dev` to start Vite with HMR on `http://127.0.0.1:5173`.

With these three processes running, you have a hot-reloading backend, dynamic CSS, and React HMR.

---

### Deployment Readiness

- **Readiness**: **Partially ready**

The project has:

- Robust production settings, including security hardening and Sentry integration.
- A CI pipeline that enforces tests, linting, type checks, and frontend builds.
- Dockerfiles and an AWS/Kubernetes-oriented deployment guide.

But it still needs:

- A concrete, committed compose file (or equivalent) that orchestrates all runtime services.
- Provider-specific deployment recipes (e.g. Railway, Render, Fly.io) and environment setup docs.
- Comprehensive E2E validation of advanced booking, payments, and real-time features in staging.

---

### Next Recommended Engineering Tasks

- **Local & DX**
  - Finalise and commit a `docker-compose.yml` (or `docker-compose.local.yml`) that matches the documented architecture.
  - Add documentation specific to the React/Vite frontend (structure, env vars, integration points).
  - Add sample data fixtures and a documented `loaddata`-based demo flow.

- **Quality & Observability**
  - Expand end-to-end tests for main user journeys (bookings, payments, schedules).
  - Configure and document monitoring/metrics (e.g. Prometheus, provider-native metrics).
  - Create runbooks for incident response, backup/restore, and rollback.

- **Deployment**
  - Implement and test a concrete PaaS deployment (e.g. Railway) using the plan in `docs/deployment_readiness.md`.
  - Harden production configs (admin URL, ALLOWED_HOSTS, CSRF/SESSION settings) and verify with `python manage.py check --deploy` in the target environment.

