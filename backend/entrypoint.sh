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
  echo "Fixture file found: portfolio_data.json"
  echo "Checking production database..."

  # Query database for Project counts
  PROJECT_COUNT=$(python -c "
import os, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
    from projects.models import Project
    print(Project.objects.count())
except Exception as e:
    sys.stderr.write(f'Database check failed: {e}\n')
    sys.exit(2)
")
  RESULT=$?

  if [ $RESULT -eq 0 ]; then
    echo "Projects found: $PROJECT_COUNT"
    if [ "$PROJECT_COUNT" -eq 0 ]; then
      echo "Loading portfolio_data.json..."
      if python manage.py loaddata portfolio_data.json; then
        echo "loaddata completed successfully"
        echo "Production data verification:"
        VERIFY_OUTPUT=$(python -c "
import os, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
    from portfolio.models import Profile, Skill
    from projects.models import Project
    from experience.models import Experience
    from education.models import Education
    from certificates.models import Certificate
    profiles = Profile.objects.count()
    skills = Skill.objects.count()
    projects = Project.objects.count()
    experience = Experience.objects.count()
    education = Education.objects.count()
    certificates = Certificate.objects.count()
    print(f'Profiles: {profiles}')
    print(f'Skills: {skills}')
    print(f'Projects: {projects}')
    print(f'Experience: {experience}')
    print(f'Education: {education}')
    print(f'Certificates: {certificates}')
    if profiles < 1 or skills < 10 or projects < 1:
        sys.stderr.write('Verification failed: Expected records are missing!\n')
        sys.exit(3)
except Exception as e:
    sys.stderr.write(f'Verification query failed: {e}\n')
    sys.exit(2)
")
        VERIFY_RESULT=$?
        if [ $VERIFY_RESULT -eq 0 ]; then
          echo "$VERIFY_OUTPUT"
          echo "Verification completed successfully"
        else
          echo "$VERIFY_OUTPUT" >&2
          echo "ERROR: Database verification failed after loaddata!" >&2
          exit 1
        fi
      else
        echo "ERROR: loaddata failed" >&2
        exit 1
      fi
    else
      echo "Database already contains projects. Skipping loaddata."
    fi
  else
    echo "ERROR: Failed to query database during startup. Aborting deployment." >&2
    exit 1
  fi
else
  echo "Fixture file NOT found: portfolio_data.json. Skipping initialization."
fi


# Collect static files
python manage.py collectstatic --no-input --clear

# Start Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2 --timeout 120
