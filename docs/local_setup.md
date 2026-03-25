## Local Development Setup (with Hot Reload)

This guide describes how to run Wellness Solutions locally with hot reload for:

- **Django backend** (auto-reload on Python/template changes)
- **Django theme/Tailwind** (CSS auto-rebuild)
- **React/Vite frontend** (HMR on React components)

> **Note**: In this environment I cannot execute shell or Docker commands directly, so the steps below are based on the project’s own documentation and configuration. You should run them in your own terminal.

---

### 1. Prerequisites

- **OS**: macOS, Linux, or Windows (WSL2 recommended on Windows)
- **Backend**
  - Python **3.11** (matches Docker image and CI)
  - PostgreSQL **13+**
  - Redis **6+**
- **Frontend / assets**
  - Node.js **20+**
  - `pnpm` (recommended, matches CI) or `npm`
- **Optional (but recommended)**
  - Docker Desktop (for running Postgres/Redis via containers or full stack with Compose)
  - `git`

---

### 2. Option A — Full Docker Stack (recommended on WSL)

This option runs Django + Postgres + Redis + Mailpit in Docker, with hot reload on code changes via a bind mount. You still run the React/Vite dev server and Tailwind watchers from WSL for best HMR performance.

#### 2.1. Ensure Docker is available in WSL

From your WSL Ubuntu shell:

```bash
docker version
```

If this fails, enable WSL integration for Ubuntu in Docker Desktop on Windows.

#### 2.2. Build and start the local stack

From the project root (`wellness_solutions`):

```bash
docker compose -f docker-compose.local.yml up --build
```

What this does:

- Builds the `web` service from `compose/local/django/Dockerfile`.
- Starts:
  - `web` (Django, using `config.settings.local`, hot reload via `/app` volume)
  - `postgres` (PostgreSQL 15, DB `wellness_solutions`)
  - `redis` (Redis 6)
  - `mailpit` (SMTP + web UI for dev email)

Key access points:

- **Backend**: `http://127.0.0.1:8000`
- **Admin**: `http://127.0.0.1:8000/admin/`
- **Mailpit UI**: `http://127.0.0.1:8025`

#### 2.3. Create a superuser inside the container

In another WSL terminal, from the project root:

```bash
docker compose -f docker-compose.local.yml exec web python manage.py createsuperuser
```

Follow the prompts (email, password). This account will be used for admin/demo.

> **Hot reload note**: Because `.` is mounted into `/app` in the `web` container, editing Python or template files on your host will trigger Django’s auto‑reload inside the container.

#### 2.4. Run Tailwind and Vite from WSL

While Docker handles backend + DB + Redis + Mailpit, run the asset pipelines from WSL for fast HMR:

- **Tailwind/theme (CSS hot reload)**

  ```bash
  cd theme/static_src
  pnpm install   # or: npm install
  pnpm run dev
  ```

- **React/Vite frontend (SPA hot reload)**

  ```bash
  cd frontend
  pnpm install   # or: npm install
  echo 'VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1' > .env.local
  pnpm dev
  ```

You now have:

- Django API + admin in Docker on `http://127.0.0.1:8000`
- Mailpit in Docker on `http://127.0.0.1:8025`
- React SPA with HMR on `http://127.0.0.1:5173`

---

### 3. Option B — Pure Host Setup (non‑Docker)

If you prefer to run everything directly on your machine instead of Docker, follow this path.

#### 3.1. Clone and Create Virtual Environment

```bash
git clone <your-repo-url> wellness_solutions
cd wellness_solutions

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

---

### 4. Install Python Dependencies

Use the local requirements bundle, which includes dev and tooling dependencies:

```bash
pip install --upgrade pip
pip install -r requirements/local.txt
```

---

### 5. Start PostgreSQL and Redis

You can either use locally installed services or run them via Docker.

#### Option A: Docker containers (recommended for quick start)

```bash
# PostgreSQL
docker run --name jpf-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=wellness_solutions \
  -p 5432:5432 \
  -d postgres:15

# Redis
docker run --name jpf-redis \
  -p 6379:6379 \
  -d redis:6
```

#### Option B: Local services

- Create a database named `wellness_solutions` in your local Postgres instance.
- Ensure Redis is running on `localhost:6379`.

---

### 6. Configure Environment Variables

The Django settings use `django-environ` and expect a `DATABASE_URL` and `REDIS_URL`. To load them from a `.env` file in development, also enable `DJANGO_READ_DOT_ENV_FILE`.

Create a `.env` in the project root:

```bash
touch .env
```

Example contents:

```bash
DJANGO_READ_DOT_ENV_FILE=True
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=change-me-dev-secret

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wellness_solutions
REDIS_URL=redis://localhost:6379/0

DJANGO_ACCOUNT_ALLOW_REGISTRATION=True
DJANGO_SITE_NAME="Wellness Solutions (Local)"
DJANGO_SITE_URL="http://localhost:8000"
```

Alternatively, you can export these in your shell instead of using `.env`.

---

### 7. Apply Database Migrations and Create Superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

Follow the prompts to set up an admin account.

---

### 8. Backend Dev Server (Django with Auto-Reload)

For basic hot reload on Python and template changes, the standard Django dev server is enough:

```bash
python manage.py runserver 0.0.0.0:8000
```

If you prefer `runserver_plus` from `django-extensions` (already installed and wired in the Docker `start` script):

```bash
python manage.py runserver_plus 0.0.0.0:8000
```

This server:

- Auto-reloads when Python files or templates change.
- Serves the core HTML templates and backend API at `http://127.0.0.1:8000/`.

Keep this terminal open while developing.

---

### 9. Tailwind / Theme Hot Reload (Django templates & CSS)

The `theme/static_src` project builds and watches Tailwind/SCSS assets.

#### Install theme dev dependencies

```bash
cd theme/static_src
pnpm install   # or: npm install
```

#### Start Tailwind/watchers (hot reload for CSS)

```bash
pnpm run dev   # or: npm run dev
```

This runs:

- `sass --watch` to compile `src/styles.scss` into `../static/css/dist/styles.css`
- `postcss --watch` on the compiled CSS

As you edit `src/styles.scss` or other imported styles, CSS is rebuilt automatically; Django will serve the updated static files (with debug/static settings).

---

### 10. Frontend SPA (React + Vite Hot Reload)

The `frontend/` directory contains a React + Vite app that talks to the Django API.

#### Install frontend dependencies

```bash
cd frontend
pnpm install   # or: npm install
```

#### Configure API base URL (if needed)

Create a `.env.local` (or `.env.development`) file inside `frontend/` to point to your local backend:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Only variables prefixed with `VITE_` are exposed to the client (see `vite.config.ts`).

#### Start Vite dev server with HMR

```bash
pnpm dev   # or: npm run dev
```

The Vite server:

- Runs on `http://127.0.0.1:5173` by default.
- Provides full hot module replacement (HMR) for React components and CSS.
- Is already configured in `vite.config.ts` with:
  - `host: true` (accessible via LAN if needed)
  - `port: 5173`

Keep this terminal open as well.

---

### 11. CORS and Cross-Origin Setup

The local Django settings (`config/settings/local.py`) already allow the Vite origin:

- `http://localhost:5173`
- `http://127.0.0.1:5173`

So with:

- Backend at `http://127.0.0.1:8000`
- Frontend at `http://127.0.0.1:5173`

the React app can call the Django API without additional configuration.

---

### 12. Recommended Terminal Layout

For smooth hot-reload development:

1. **Terminal 1 (backend)**
   - `source .venv/bin/activate` (or Windows equivalent)
   - `python manage.py runserver_plus 0.0.0.0:8000`
2. **Terminal 2 (theme/Tailwind)**
   - `cd theme/static_src`
   - `pnpm install` (first time only)
   - `pnpm run dev`
3. **Terminal 3 (frontend SPA)**
   - `cd frontend`
   - `pnpm install` (first time only)
   - `pnpm dev`

You now have:

- Django + API with auto-reload on `http://127.0.0.1:8000/`
- Tailwind/theme CSS auto-compiling
- React SPA with full HMR on `http://127.0.0.1:5173/`

---

### 13. Demo Instructions & Smoke Tests Before a Client Demo

Once everything is running, validate key flows manually:

- **Authentication**
  - Visit `http://127.0.0.1:8000/admin/` and log in as the superuser you created.
  - Confirm login, logout, and password reset flow (email via Mailpit if you use the Docker Mailpit setup).
- **Core domain**
  - Create a test `Organization`, `Location`, `Service`, and `Instructor` via the admin or React UI.
  - Create a **Booking** and ensure:
    - Availability/validation checks work.
    - Price, discount, and total price fields behave as expected.
- **Frontend**
  - Load the React app at `http://127.0.0.1:5173` and confirm:
    - Dashboard pages render.
    - Navigation and forms work.
    - API calls succeed (no CORS or 401 errors once authenticated).
- **Performance / stability (basic)**
  - Quickly navigate between multiple pages to ensure no obvious crashes or severe slowdowns.

Document any errors you see so they can be fixed before the client demo.

---

### 14. Known Gaps / Caveats

- This guide assumes Postgres and Redis are reachable as configured; if your environment differs (e.g. non-standard ports, Docker networks), adjust `DATABASE_URL` and `REDIS_URL` accordingly.
- WebSockets, calendar integrations, and payment gateways are more complex subsystems; they should be tested separately once the basic flows are stable.
- In this audit environment, tests and servers could not be executed directly; use the test commands from `README.md` and `docs/testing.rst` to validate your own instance:

```bash
pytest
pytest --cov=wellness_solutions
mypy .
ruff check .
```

