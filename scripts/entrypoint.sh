#!/bin/sh

# Fail immediately if any command fails
set -e

# --- 0. GIT SAFE DIRECTORY WORKAROUND (MOVED TO TOP) ---
# This ensures that tools like pre-commit can access the volume-mounted Git repository
# without throwing the "fatal: unsafe repository" error when run via 'docker exec'.
git config --global --add safe.directory /app || true


# --- 1. Set Django Settings Module ---
# Use environment variable if set, otherwise fallback to default settings.
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-ChronosAtlas.settings_default}"

# --- 2. Use hardcoded DB credentials for pg_isready ---
# These MUST match the 'db' service credentials in docker-compose.prod.yml
DB_HOST="db"
DB_PORT="5432"
DB_USER="chronosuser"
PGPASSWORD="chronospassword"
DB_NAME="chronosatlas"

# --- 3. Wait for PostgreSQL to be ready ---
echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Loop until pg_isready reports success (exit code 0)
until PGPASSWORD=$PGPASSWORD pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t 1; do
    echo "PostgreSQL is unavailable - sleeping for 1 second..."
    sleep 1
done

echo "PostgreSQL is up and running! Proceeding to server startup."


# --- 4. Run migrations and load MVP data ---
# If the command is makemigrations or migrate (even as python manage.py ...), skip migrations/data load here
if { [ "$1" = "makemigrations" ] || [ "$1" = "migrate" ]; } || \
   { [ "$1" = "python" ] && [ "$2" = "manage.py" ] && { [ "$3" = "makemigrations" ] || [ "$3" = "migrate" ]; }; }; then
    echo "Entrypoint: Skipping migrations and data load for migration command."
else
    echo "Running migrations..."
    python manage.py migrate --noinput

    # Load initial development data after successful migrations
    if [ "$DJANGO_SETTINGS_MODULE" != "ChronosAtlas.settings_prod" ]; then
        echo "Loading MVP data..."
        python manage.py load_mvp_data
    fi
fi

# Only collect static files in production
if [ "$DJANGO_SETTINGS_MODULE" = "ChronosAtlas.settings_prod" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
else
    echo "Skipping collectstatic (not production settings)"
fi

# --- 5. Execute the Main Command ---
# This logic checks if any command was passed to the entrypoint.
# If arguments exist (e.g., `python manage.py runserver`), it executes them.
# If no arguments are provided, it defaults to starting the Gunicorn server.
if [ -n "$1" ]; then
    echo "Executing command: $@"
    exec "$@"
else
    echo "Starting Gunicorn server..."
    exec python -m gunicorn ChronosAtlas.wsgi:application --bind 0.0.0.0:8000
fi
