#!/bin/bash
# Wellness Solutions — Thursday Demo Startup Script
# Run from: /home/meshack/development/Work/wellness_solutions/

echo "🚀 Starting Wellness Solutions Demo..."

# Terminal 1: Django Backend
echo ""
echo "▶▶ Backend (Django)"
echo "cd /home/meshack/development/Work/wellness_solutions"
echo "source venv/bin/activate && python manage.py runserver 0.0.0.0:8000"
echo ""

# Terminal 2: React Frontend
echo "▶▶ Frontend (Vite)"
echo "cd /home/meshack/development/Work/wellness_solutions/frontend"
echo "pnpm run dev"
echo ""

echo "Backend will be at: http://localhost:8000"
echo "Frontend will be at: http://localhost:5173"
echo ""
echo "Demo user flow:"
echo "  1. Open localhost:5173"
echo "  2. Click 'Get Started' -> Register a new account"
echo "  3. Get taken to /dashboard automatically"
echo "  4. Click '+ Book New' -> choose a session -> confirm"
echo "  5. See booking in /bookings"
echo "  6. For admin: login with staff account -> /admin shows analytics"
