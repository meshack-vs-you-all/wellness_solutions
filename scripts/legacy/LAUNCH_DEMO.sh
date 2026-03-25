#!/bin/bash

# Wellness Solutions - One-Click Demo Launcher
# ----------------------------------------
# This script starts the backend and frontend for the live demo.
# Run this BEFORE the client joins.

echo "🚀 Preparing Wellness Solutions Demo Environment..."

# 1. Kill existing processes to avoid port conflicts
echo "🛑 Cleaning up old processes..."
lsof -i :8000,5173 | awk 'NR>1 {print $2}' | xargs kill -9 2>/dev/null

# 2. Environment Variables
export DATABASE_URL=sqlite:///db.sqlite3
export DJANGO_SETTINGS_MODULE=config.settings.local
export DJANGO_READ_DOT_ENV_FILE=True
export USE_DOCKER=no

# 3. Start Backend (Django)
echo "📦 Starting Backend (Port 8000)..."
source demo-env/bin/activate
python manage.py collectstatic --no-input --clear > /dev/null 2>&1
python manage.py runserver 0.0.0.0:8000 > demo_backend.log 2>&1 &
BACKEND_PID=$!

# 4. Start Frontend (Vite)
echo "🎨 Starting Frontend (Port 5173)..."
cd frontend
pnpm dev -- --host > ../demo_frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# 5. Final Checks
sleep 5
echo "----------------------------------------"
echo "✅ DEMO IS LIVE!"
echo "----------------------------------------"
echo "🖥️  Frontend: http://localhost:5173"
echo "⚙️  Backend:  http://localhost:8000"
echo "📊 Logs:      tail -f demo_backend.log"
echo "----------------------------------------"
echo "Press Ctrl+C to stop both services when demo is over."

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; echo '🛑 Demo Stopped.'; exit" INT
wait
