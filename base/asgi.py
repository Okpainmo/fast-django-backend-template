"""
ASGI config for base project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# ==================================================================================================================
# selecting the preferred/current working environment.
# ==================================================================================================================

# default - no longer needed
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# Split set-up due to the project's decentralized configuration. For production deployment, selection must be
# handled here(`base -> settings -> asgi.py`), inside `base -> settings -> wsgi.py` and inside `manage.py`. But
# For development(when in a local environment), selection will work even when done in only `manage.py`.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.staging')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production')

# =================================================================================================================
# selecting the preferred/current working environment.
# =================================================================================================================

application = get_asgi_application()
