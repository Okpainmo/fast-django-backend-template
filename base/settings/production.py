from .base import *

# DEBUG = False
DEBUG = True
ALLOWED_HOSTS = []

# production postgres setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB_NAME__PRODUCTION"),
        'USER': os.getenv("POSTGRES_DB_USER__PRODUCTION"),
        'PASSWORD': os.getenv("POSTGRES_DB_PASSWORD__PRODUCTION"),
        'HOST': os.getenv("POSTGRES_DB_HOST__PRODUCTION"),
        'PORT': os.getenv("POSTGRES_DB_PORT__PRODUCTION"),
    }
}

# production AWS S3 setup
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME__PRODUCTION")
AWS_BUCKET_REGION = os.getenv("AWS_BUCKET_REGION__PRODUCTION")
AWS_S3__BUCKET_BASE_URL = f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/"
