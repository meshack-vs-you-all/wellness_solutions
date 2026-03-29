# Wellness Solutions

## Project Overview

This repository now contains a WordPress-ready theme shell and a Vite/React frontend that mounts inside it. The previous Django implementation has been removed from the working tree.

## What Remains

- A Vite/React frontend in `frontend/`
- A WordPress theme shell in `wordpress/wp-content/themes/wellness-solutions/`
- Static design assets used by the current prototype
- Demo/reference material such as `DEMO_MASTER_GUIDE.pdf`

## Migration Status

- The app now supports WordPress runtime config and theme asset builds.
- Auth, booking, dashboard, and admin behaviors still depend on the WordPress plugins/endpoints you install.

## Frontend

```bash
cd frontend
npm install
npm run dev
npm run build:wordpress
```

## Recommended Next Step

Define or confirm the plugin REST namespace and authentication strategy, then map the frontend service calls to those endpoints.
