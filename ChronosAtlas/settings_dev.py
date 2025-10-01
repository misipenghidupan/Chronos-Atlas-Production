import dj_database_url

DEBUG = True
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
ROOT_URLCONF = "ChronosAtlas.urls"

# Use dj_database_url to connect to the PostgreSQL container defined in
# docker-compose.dev.yml. This ensures environment parity with production.
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://chronosuser:chronospassword@db:5432/chronosatlas",
        conn_max_age=600,
    )
}

print(">>> Loaded ChronosAtlas Development Settings (settings_dev.py)")
