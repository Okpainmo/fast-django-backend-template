from .base import *

DEBUG = True
ALLOWED_HOSTS = []

# Database - SQlite3
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# dev postgres setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB_NAME__DEV"),
        'USER': os.getenv("POSTGRES_DB_USER__DEV"),
        'PASSWORD': os.getenv("POSTGRES_DB_PASSWORD__DEV"),
        'HOST': os.getenv("POSTGRES_DB_HOST__DEV"),
        'PORT': os.getenv("POSTGRES_DB_PORT__DEV"),
    }
}

# dev AWS S3 setup
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME__DEV")
AWS_BUCKET_REGION = os.getenv("AWS_BUCKET_REGION__DEV")
AWS_S3__PUBLIC_FILE_BASE_URL = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com"
