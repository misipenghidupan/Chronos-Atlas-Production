#!/bin/sh

# Fail immediately if any command fails
set -e

# --- 0. NO HARDCODED SETTINGS ---
# We deliberately REMOVE the line 'export DJANGO_SETTINGS_MODULE=...'
# The correct settings file (dev or prod) will be read from the environment 
# variables passed by the specific docker-compose override file.

# --- 1. Use environment variables for DB credentials (from docker-compose) ---
# Ensure default environment variables are set for safety if they aren't provided
# Using : before the variable to ensure the default is set if the variable is missing
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${DB_USER:=chronosuser}"
: "${PGPASSWORD:=chronospassword}"
: "${DB_NAME:=chronosatlas}"

# --- 2. Wait for PostgreSQL to be ready ---
echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Loop until pg_isready reports success (exit code 0)
until PGPASSWORD=$PGPASSWORD pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t 1; do
    echo "PostgreSQL is unavailable - sleeping for 1 second..."
    sleep 1
done

echo "PostgreSQL is up and running! Proceeding to setup."

# --- 3. Run migrations and collect static files ---
# These commands now rely entirely on the DJANGO_SETTINGS_MODULE 
# environment variable being set correctly by Docker Compose.
echo "Running migrations..."
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput

# --- 4. Execute the Main Command: (Starts runserver or gunicorn) ---
# The "$@" variable holds the 'command' defined in the specific docker-compose file.
echo "Executing main Docker command: $@"
exec "$@"
