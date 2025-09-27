import os
from .settings import * # Import base settings first

# Standard Production Settings Overrides
DEBUG = False

# REQUIRED for production security
# In a production environment, you should replace '*' with your specific domain name(s).
ALLOWED_HOSTS = ['*']

# --- SSL/HTTPS FIX: DISABLE SSL REDIRECT FOR LOCAL HTTP TESTING ---
# We MUST disable these settings to allow plain HTTP traffic in the container
# when no external proxy (like Nginx) is handling SSL termination.
SECURE_SSL_REDIRECT = False 
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
# ------------------------------------------------------------------

# --- CRITICAL FIX: Configure Logging to output full tracebacks to stdout/stderr in Docker ---
# When DEBUG=False, Django normally swallows tracebacks. This forces all errors
# to the console handler so they appear in 'docker compose logs -f api'.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Define a console handler
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Default Django logger (for general messages)
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        # Root logger: catches everything not caught by others, ensuring application errors are logged
        '': {
            'handlers': ['console'],
            'level': 'DEBUG', # Set to DEBUG to catch the most detailed info, including tracebacks
            'propagate': True,
        },
        # Specific logger for GraphQL errors (highly recommended for Graphene apps)
        'graphene.execution.errors': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

print(">>> Loaded ChronosAtlas Production Settings (settings_prod.py) - SecurityMiddleware removed, redirects disabled, logging enabled.")
