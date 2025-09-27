#!/bin/sh

# Fail immediately if any command fails
set -e

# Extract DB connection details from environment variables
# We use standard PGDATABASE, PGUSER, PGHOST, PGPORT for pg_isready
DB_HOST=$(echo $DATABASE_URL | awk -F'[@/:]' '{print $7}')
DB_PORT=5432
DB_USER=$(echo $DATABASE_URL | awk -F'[@/]' '{print $3}')
DB_NAME=$(echo $DATABASE_URL | awk -F'[@/]' '{print $4}')
PGPASSWORD=$(echo $DATABASE_URL | awk -F'[:@]' '{print $4}')

# --- Wait for PostgreSQL to be ready ---
echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Loop until pg_isready reports success (exit code 0)
until PGPASSWORD=$PGPASSWORD pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t 1; do
  echo "PostgreSQL is unavailable - sleeping for 1 second..."
  sleep 1
done

echo "PostgreSQL is up and running!"

# --- Run Migrations and Collect Static Files ---

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Load initial data (only needed once for a clean DB)
# Note: You might want to run this manually or conditionally
# echo "Loading initial MVP data..."
# python manage.py load_mvp_data

# --- Execute the Main Command ---
# Executes the command provided in the Dockerfile CMD instruction (Gunicorn)
echo "Starting Gunicorn server..."
exec "$@"
