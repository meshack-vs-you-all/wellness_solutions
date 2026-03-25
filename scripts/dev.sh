#!/bin/bash

# Wellness Solutions - Consolidated Development Runner
# ------------------------------------------------
# This script starts both the Django backend and the Vite frontend.

PROJECT_ROOT="/home/meshack/src/work/wellness_solutions"
VENV_DIR="$PROJECT_ROOT/venv_new"
PYTHON="$VENV_DIR/bin/python"

echo "🚀 Starting Wellness Solutions Development Environment..."

# 1. Cleanup existing processes
echo "🛑 Cleaning up old processes on ports 8000 and 5173..."
lsof -i :8000,5173 | awk 'NR>1 {print $2}' | xargs kill -9 2>/dev/null || true

# 2. Set Environment Variables
export DJANGO_READ_DOT_ENV_FILE=True
export DATABASE_URL=sqlite:///db.sqlite3
export USE_DOCKER=no
export DJANGO_SETTINGS_MODULE=config.settings.local

# 3. Start Backend
echo "📦 Starting Django Backend (Port 8000)..."
cd "$PROJECT_ROOT"
# Ensure migrations are applied
$PYTHON manage.py migrate --no-input
# Start server in background
nohup $PYTHON manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &
BACKEND_PID=$!

# 4. Start Frontend
echo "🎨 Starting Vite Frontend (Port 5173)..."
cd "$PROJECT_ROOT/frontend"
# Check for pnpm or npm
if command -v pnpm &> /dev/null; then
    nohup pnpm dev -- --host 0.0.0.0 > ../frontend.log 2>&1 &
else
    nohup npm run dev -- --host 0.0.0.0 > ../frontend.log 2>&1 &
fi
FRONTEND_PID=$!

echo "----------------------------------------"
echo "✅ SERVICES ARE STARTING!"
echo "----------------------------------------"
echo "🖥️  Frontend: http://localhost:5173"
echo "⚙️  Backend:  http://localhost:8000"
echo "📊 Logs:      tail -f backend.log frontend.log"
echo "----------------------------------------"
echo "PIDs: Backend=$BACKEND_PID, Frontend=$FRONTEND_PID"
echo "Press Ctrl+C to stop this watcher (services will keep running in background)."

# Trap exit to show status but keep services running
trap "echo 'Watcher stopped. Services are still running in background.'; exit" INT
wait
