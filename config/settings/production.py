from .base import *
import os
import boto3
#DJANGO_SETTINGS_MODULE = 'config.settings.production'


SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST')]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("POSTGRES_ENGIN"),
        'NAME': os.environ.get("POSTGRES_NAME"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

<<<<<<< HEAD


SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")
=======
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
SMTP_USER_NAME = os.environ.get("EMAIL_HOST_USER")
SMTP_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

AWS_SES_REGION_NAME = 'ap-northeast-1'
AWS_SES_REGION_ENDPOINT = os.environ.get("AWS_SES_REGION_ENDPOINT")
AWS_SES_ACCESS_KEY_ID = os.environ.get("AWS_SES_ACCESS_KEY_ID")
AWS_SES_SECRET_ACCESS_KEY = os.environ.get("AWS_SES_SECRET_ACCESS_KEY")
AWS_SES_AUTO_THROTTLE = 0.5 
>>>>>>> origin/master

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = 'ap-northeast-1'
AWS_DEFAULT_ACL = None
S3_USE_SIGV4 = True

AWS_CLOUD_FRONT_CNAME = 'd2c1s3ifu98bmb'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_CLOUD_FRONT_CNAME}.cloudfront.net'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

STATIC_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATIC_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, PUBLIC_MEDIA_LOCATION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DOWNLOAD_DIST_ID = os.environ.get("DOWNLOAD_DIST_ID")
key_pair_id = os.environ.get("key_pair_id")
