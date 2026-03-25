#!/bin/bash
echo "🚀 Starting Django Backend..."
export DJANGO_READ_DOT_ENV_FILE=True
export DATABASE_URL=sqlite:///db.sqlite3
export USE_DOCKER=no
export DJANGO_SETTINGS_MODULE=config.settings.local

VENV_DIR="/home/meshack/src/work/wellness_solutions/venv_new"
PYTHON="$VENV_DIR/bin/python"

echo "Installing dependencies..."
$PYTHON -m pip install -r requirements/base.txt --quiet
echo "Dependencies installed."

echo "Running migrations..."
$PYTHON manage.py makemigrations payments
$PYTHON manage.py migrate

echo "Collecting static files..."
$PYTHON manage.py collectstatic --no-input --clear

echo "Starting server on http://localhost:8000"
$PYTHON manage.py runserver 0.0.0.0:8000
