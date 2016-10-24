from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rr9eq3&0hhn-#%#=0$321uj=&u0p)6t4ne8s)21%)c1+-e=vyq'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'yourin_db',                      # Or path to database file if using sqlite3.
        #'NAME': 'test',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
} 

try:
    from .local import *
except ImportError:
    pass
