# ChronosAtlas/settings/prod.py

from .base import *
import dj_database_url

# PRODUCTION-SPECIFIC SETTINGS
# --------------------------------------------------------------------------

# SECURITY WARNING: Must be False!
DEBUG = False

# REQUIRED: Replace '*' with your specific domain name(s) in the ENV file!
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# --- Security Middleware and SSL Redirects ---
# Add security middleware back for prod
MIDDLEWARE.insert(0, 'django.middleware.security.SecurityMiddleware')

# CRITICAL FIX: Only set secure cookies/redirects if Nginx/Load Balancer handles SSL
# We often disable this for simple container testing, but re-enable it for cloud deployment.
SECURE_SSL_REDIRECT = True 
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# --- CRITICAL FIX: Load PostgreSQL database from DATABASE_URL environment variable ---
try:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600  # Set connection pool age
        )
    }
except Exception as e:
    print(f"Failed to load production DATABASE_URL: {e}")

# --- CRITICAL: Production Logging (copied from your old settings_prod.py) ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        '': { # Root logger
            'handlers': ['console'],
            'level': 'DEBUG', 
            'propagate': True,
        },
        'graphene.execution.errors': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# CORS SETTINGS (Restrict to actual production domains)
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://chronosatlas.com').split(',')

print(">>> Loaded ChronosAtlas Production Settings (settings.prod.py)")