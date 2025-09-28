#!/bin/sh

# Fail immediately if any command fails
set -e

# --- 0. Set Django Settings Module ---
# Ensures all Python commands use the correct production settings.
export DJANGO_SETTINGS_MODULE=ChronosAtlas.settings_prod

# --- 1. Use hardcoded DB credentials for pg_isready ---
# These MUST match the 'db' service credentials in docker-compose.prod.yml
DB_HOST="db"
DB_PORT="5432"
DB_USER="chronosuser"
PGPASSWORD="chronospassword"
DB_NAME="chronosatlas"

# --- 2. Wait for PostgreSQL to be ready ---
echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Loop until pg_isready reports success (exit code 0)
until PGPASSWORD=$PGPASSWORD pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t 1; do
    echo "PostgreSQL is unavailable - sleeping for 1 second..."
    sleep 1
done

echo "PostgreSQL is up and running! Proceeding to server startup."

# --- 3. Run migrations and collect static files ---
echo "Running migrations..."
# --noinput prevents interactive prompts (like the one for 'figures' app)
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput

# --- 4. Execute the Main Command: Start Gunicorn Server ---
echo "Starting Gunicorn server..."
exec python -m gunicorn ChronosAtlas.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --error-logfile - \
    --log-level debug