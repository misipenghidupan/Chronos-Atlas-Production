# ChronosAtlas/settings/dev.py

from .base import *
from django.conf.locale.en import formats as en_formats

# DEVELOPMENT-SPECIFIC SETTINGS
# --------------------------------------------------------------------------

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# --- Security Middleware adjustment for HTTP in Development ---
# Add security middleware back for dev
MIDDLEWARE.insert(0, 'django.middleware.security.SecurityMiddleware')

# CORS SETTINGS (allows local React/Frontend traffic)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# Optionally use SQLite for ease of setup if Postgres is not running (not recommended for this project)
# DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
# DATABASES['default']['NAME'] = BASE_DIR / 'db.sqlite3'

# Logging is verbose in dev by default, so we don't need the complex LOGGING dict here.
print(">>> Loaded ChronosAtlas Development Settings (settings.dev.py)")