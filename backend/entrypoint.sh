#!/bin/bash

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

# Collect static files
python manage.py collectstatic --no-input --clear

# Start Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2 --timeout 120
