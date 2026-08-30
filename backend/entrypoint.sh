#!/bin/bash

# On Render, fail early if DATABASE_URL is not set
if [ "$RENDER" = "true" ]; then
  if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL environment variable is not set on Render!" >&2
    exit 1
  fi
fi

# Parse database host and port dynamically if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
  DB_HOST=$(python -c "from urllib.parse import urlparse; url = urlparse('$DATABASE_URL'); print(url.hostname or '')")
  DB_PORT=$(python -c "from urllib.parse import urlparse; url = urlparse('$DATABASE_URL'); print(url.port or 5432)")
else
  DB_HOST="db"
  DB_PORT=5432
fi

if [ -n "$DB_HOST" ]; then
  echo "Waiting for postgres at $DB_HOST:$DB_PORT..."
  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.1
  done
  echo "PostgreSQL started"
else
  echo "Using local SQLite database (no network check required)"
fi


# Run migrations
python manage.py migrate --no-input

# Load portfolio fixture if no projects exist in the database and fixture is present
if [ -f "portfolio_data.json" ]; then
  if python -c "
import os, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
    from projects.models import Project
    exists = Project.objects.exists()
except Exception as e:
    sys.stderr.write(f'Database check failed: {e}\n')
    sys.exit(2)
sys.exit(0 if exists else 1)
"; then
    RESULT=0
  else
    RESULT=$?
  fi

  if [ $RESULT -eq 0 ]; then
    echo "Database already contains projects. Skipping loaddata."
  elif [ $RESULT -eq 1 ]; then
    echo "No projects found. Loading portfolio_data.json..."
    python manage.py loaddata portfolio_data.json
  else
    echo "ERROR: Failed to query database. Aborting deployment to prevent data corruption." >&2
    exit 1
  fi
fi


# Collect static files
python manage.py collectstatic --no-input --clear

# Start Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2 --timeout 120
