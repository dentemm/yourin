from __future__ import absolute_import, unicode_literals

from .base import *

try:
    from .local import *
except ImportError:
    pass

DEBUG = True

# TODO: SET EMAIL BACKEND FOR PRODUCTION
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'home.custom_storages.MediaStorage'

# WHITENOISE
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# DATABASE SETUP
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


