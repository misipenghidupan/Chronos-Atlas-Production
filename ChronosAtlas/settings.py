import os
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SECURITY SETTINGS
# ==============================================================================

# Uses python-decouple to load secrets from the .env file
SECRET_KEY = config("SECRET_KEY", default="insecure-secret-key")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=lambda v: v.split(","))


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    # Django Built-in Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third-Party Apps
    "graphene_django",
    
    # Project Apps
    "timeline",  # The application containing your models and schema
]

# FIXES ERRORS E408, E409, E410
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ChronosAtlas.urls'

# FIXES ERROR E403 (Required for Admin app)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ChronosAtlas.wsgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================

# Uses variables set in docker-compose.yml (DB_HOST: db)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="chronosatlas"),
        "USER": config("DB_USER", default="chronos_user"),
        "PASSWORD": config("DB_PASSWORD", default="chronos_pass"),
        "HOST": config("DB_HOST", default="db"),
        "PORT": config("DB_PORT", default=5432, cast=int),
    }
}


# ==============================================================================
# PASSWORD VALIDATION AND LANGUAGE
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

STATIC_URL = "/static/"
# Used by entrypoint.sh to collect static files
STATIC_ROOT = BASE_DIR / "staticfiles" 

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==============================================================================
# GRAPHENE (GraphQL) CONFIGURATION
# ==============================================================================

GRAPHENE = {
    "SCHEMA": "ChronosAtlas.schema.schema", # Points to your root schema.py file
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"