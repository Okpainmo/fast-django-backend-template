"""
WSGI config for base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# ==================================================================================================================
# the working environment(dev, staging, or production) will be set inside `manage.py`
# ==================================================================================================================

# default - no longer needed
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# split set-up due to the project's decentralized configuration - selection will be handled inside `manage.py`.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.staging')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production') 

# =================================================================================================================
# the working environment(dev, staging, or production) will be set inside `manage.py`
# =================================================================================================================

application = get_wsgi_application()
