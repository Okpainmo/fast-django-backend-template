#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # ==================================================================================================================
    # selecting the preferred/current working environment.
    # ==================================================================================================================

    # default - no longer needed
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

    # split set-up due to the project's decentralized configuration - for production deployment, selection must be 
    # handled here(`manage.py`), inside `base -> settings -> wsgi.py` and inside `base -> settings -> asgi.py`. But
    # for development(when in a local environment), selection will work even when done in only this file(`manage.py`).
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development')
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.staging')
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production') 

    # =================================================================================================================
    # selecting the preferred/current working environment.
    # =================================================================================================================

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
