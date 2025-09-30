# ChronosAtlas/settings/base.py

import os
from pathlib import Path
import dj_database_url # Keep this here for connection flexibility

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'o-7=k-r7c1&d-d!v+v229x#1@g38e!7!k+s#+@^42j975%^7b7&y')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres', # Added this based on your stack
    
    # Third-party apps
    'graphene_django',
    'corsheaders',

    # Your Project Apps
    'timeline',
    'figures',
]

MIDDLEWARE = [
    # NOTE: SecurityMiddleware is handled later because of SSL redirect logic
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Added for CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ChronosAtlas.urls'

# ... (TEMPLATES, AUTH_PASSWORD_VALIDATORS, etc. copied directly from old settings.py)

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
# CRITICAL: Define a base STATIC_ROOT. Prod will override this path for Gunicorn access.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# GRAPHENE CONFIGURATION (CRITICAL FIX)
GRAPHENE = {
    'SCHEMA': 'ChronosAtlas.schema.schema'
}

# --- Shared Database Configuration ---
# Use a flexible environment variable approach as a fallback.
# This will be overridden entirely by the DATABASE_URL in production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'chronosatlas'),
        'USER': os.environ.get('DB_USER', 'chronosuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'chronospassword'),
        'HOST': os.environ.get('DB_HOST', 'db'), # 'db' is the Docker service name
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}