import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from .settings_base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

print('>>> Loaded ChronosAtlas Development Settings (settings_dev.py)')
