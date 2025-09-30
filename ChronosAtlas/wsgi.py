"""
WSGI config for ChronosAtlas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# CRITICAL FIX: Update the settings module path to point to the default settings file.
# The Docker Compose file will override this with 'ChronosAtlas.settings.prod'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChronosAtlas.settings.dev')

application = get_wsgi_application()