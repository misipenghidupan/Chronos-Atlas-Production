import dj_database_url

# Import all required settings from the base file
# This is necessary because Django's SystemCheck needs these variables
# to be defined at the module level (not via __getattr__).
from .settings_base import *  # noqa: F403, F401

# DEVELOPMENT-SPECIFIC OVERRIDES
# Any setting defined here overrides the value imported from settings_base.

DEBUG = True
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
# The original file set ROOT_URLCONF here, we'll keep it for clarity.
ROOT_URLCONF = "ChronosAtlas.urls"


# INSTALLED_APPS is imported and correctly defined in settings_base.


# Use dj_database_url to connect to the PostgreSQL container defined in
# docker-compose.dev.yml. This ensures environment parity with production.
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://chronosuser:chronospassword@db:5432/chronosatlas",
        conn_max_age=600,
    )
}

# The __getattr__ function has been removed as all necessary base settings
# are now imported explicitly above.

print(">>> Loaded ChronosAtlas Development Settings (settings_dev.py)")
