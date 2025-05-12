"""
WSGI config for base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# ==================================================================================================================
# selecting the preferred/current working environment.
# ==================================================================================================================

# default - no longer needed
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# split set-up due to the project's decentralized configuration - for production deployment, selection must be 
# handled here(`base -> settings -> wsgi.py`), inside `base -> settings -> asgi.py` and inside `manage.py`. But
# for development(when in a local environment), selection will work even when done in only `manage.py`.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.staging')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production') 

# =================================================================================================================
# selecting the preferred/current working environment.
# =================================================================================================================

application = get_wsgi_application()
