from .base import *

DEBUG = True
ALLOWED_HOSTS = []

# production postgres setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB_NAME__STAGING"),
        'USER': os.getenv("POSTGRES_DB_USER__STAGING"),
        'PASSWORD': os.getenv("POSTGRES_DB_PASSWORD__STAGING"),
        'HOST': os.getenv("POSTGRES_DB_HOST__STAGING"),
        'PORT': os.getenv("POSTGRES_DB_PORT__STAGING"),
    }
}

# staging AWS S3 setup
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME__STAGING")
AWS_BUCKET_REGION = os.getenv("AWS_BUCKET_REGION__STAGING")
AWS_S3__BUCKET_BASE_URL = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/"
