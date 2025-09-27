#!/bin/sh

# Fail immediately if any command fails
set -e

# --- 0. Set Django Settings Module ---
# CRITICAL FIX: Explicitly set the DJANGO_SETTINGS_MODULE environment variable.
# This ensures all subsequent Python commands (migrate, collectstatic, gunicorn)
# reliably use the correct production settings file.
export DJANGO_SETTINGS_MODULE=ChronosAtlas.settings_prod

# --- 1. Extract DB connection details from DATABASE_URL using awk ---
# URL format is: postgres://USER:PASSWORD@HOST:PORT/NAME
# We must use the correct indices determined by your environment:
DB_USER=$(echo "$DATABASE_URL" | awk -F'[@/:]' '{print $4}')     # Expected to grab USER
PGPASSWORD=$(echo "$DATABASE_URL" | awk -F'[@/:]' '{print $5}')  # Expected to grab PASSWORD
DB_HOST=$(echo "$DATABASE_URL" | awk -F'[@/:]' '{print $6}')     # Expected to grab HOST (should be 'db')
DB_PORT=$(echo "$DATABASE_URL" | awk -F'[@/:]' '{print $7}')     # Expected to grab PORT (should be '5432')
DB_NAME=$(echo "$DATABASE_URL" | awk -F'[@/:]' '{print $8}')     # Expected to grab NAME

# --- IMPORTANT CHECK ---
if [ -z "$DB_USER" ] || [ -z "$DB_HOST" ] || [ -z "$DB_NAME" ]; then
    echo "CRITICAL ERROR: Missing essential database parameters (User, Host, or Name) after shell parsing."
    echo "Full DATABASE_URL being parsed: $DATABASE_URL"
    echo "Parsed values: User='$DB_USER', Password='<REDACTED>', Host='$DB_HOST', Port='$DB_PORT', Name='$DB_NAME'"
    exit 1
fi

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
# Removed --settings argument; now uses DJANGO_SETTINGS_MODULE env var.
python manage.py migrate --noinput
echo "Collecting static files..."
# Removed --settings argument; now uses DJANGO_SETTINGS_MODULE env var.
python manage.py collectstatic --noinput

# --- 4. Execute the Main Command: Start Gunicorn Server ---
echo "Starting Gunicorn server..."
# FIX: Added --error-logfile - to force error tracebacks to be logged to stdout/stderr.
# NEW FIX: Added --log-level debug to force Gunicorn to output detailed application errors.
exec python -m gunicorn ChronosAtlas.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --error-logfile - \
    --log-level debug
