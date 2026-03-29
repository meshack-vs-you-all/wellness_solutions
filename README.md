# Wellness Solutions

This repository now contains a WordPress-ready theme shell plus the retained React frontend that mounts inside it.

## Current State

- `frontend/` contains the retained Vite React app and design/reference UI.
- `wordpress/wp-content/themes/wellness-solutions/` contains the WordPress theme shell that enqueues the built frontend.
- `DEMO_MASTER_GUIDE.pdf` is kept as a demo/reference document.
- The previous Django backend, SQLite database, Celery logs, Docker backend files, and Django templates have been removed from the working tree.

## What Is Not Done Yet

- Authentication, bookings, dashboards, and admin flows still depend on the WordPress plugins/endpoints you install.
- You will need to map the plugin routes to the app's configured REST namespace if they differ.

## WordPress Theme

The theme lives at:

```bash
wordpress/wp-content/themes/wellness-solutions
```

The React app builds into:

```bash
wordpress/wp-content/themes/wellness-solutions/assets/app
```

## Frontend

Run the frontend locally:

```bash
cd frontend
npm install
npm run dev
npm run build:wordpress
```

## Reproduce On Another Machine

Clone the repository and build the theme bundle:

```bash
git clone https://github.com/meshack-vs-you-all/wellness_solutions.git
cd wellness_solutions/frontend
npm install
npm run build:wordpress
```

This produces the frontend assets inside:

```bash
wordpress/wp-content/themes/wellness-solutions/assets/app
```

## Local WordPress Wiring

This repo now includes a reproducible local stack:

```bash
cp .env.wordpress.example .env.wordpress
bash scripts/local-wordpress-up.sh
```

That script:

1. installs frontend dependencies if needed
2. builds the WordPress theme bundle
3. starts MariaDB and WordPress with Docker Compose
4. bootstraps WordPress through WP-CLI
5. activates the `Wellness Solutions` theme
6. creates an app shell page at `/wellness-app/`

Useful commands:

```bash
bash scripts/local-wordpress-up.sh
bash scripts/local-wordpress-down.sh
bash scripts/local-wordpress-reset.sh
FORCE_FRONTEND_BUILD=1 bash scripts/local-wordpress-up.sh
```

Default local URLs:

- site: `http://127.0.0.1:8090/`
- admin: `http://127.0.0.1:8090/wp-admin/`
- app shell: `http://127.0.0.1:8090/wellness-app/`

Plugin work still remains:

1. Install the booking, auth, and admin plugins you plan to use.
2. Expose the plugin routes through the expected namespace or update the runtime config in the theme if your namespace differs from `/wp-json/wellness-solutions/v1`.

## CI And Validation

- GitHub Actions now validates the current stack in `.github/workflows/predeploy.yml`.
- The workflow runs `npm ci`, `npm exec tsc --noEmit`, `npm run build:wordpress`, checks for the generated Vite manifest, and lints the theme PHP files.
- Built assets are intentionally ignored from Git. Another machine must run the frontend build step before activating the theme.

## Next Step

1. Install your WordPress plugins.
2. Point the app at the plugin REST namespace if it is not `/wp-json/wellness-solutions/v1`.
3. Build the frontend into the theme with `npm run build:wordpress`.
4. Activate the `Wellness Solutions` theme or use the `Wellness App Shell` page template.
