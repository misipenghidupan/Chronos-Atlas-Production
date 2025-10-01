import os

from .settings_base import BASE_DIR

# Default settings file for regular (non-dev, non-prod) usage
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
}

print(">>> Loaded ChronosAtlas Default Settings (settings_default.py)")
