"""
WSGI config for library_app project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/gunicorn/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_app.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
