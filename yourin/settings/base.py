"""
Django settings for yourin project.

Generated by 'django-admin startproject' using Django 1.9.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

SECRET_KEY = '!4e7cfxq_!(8g(*w^f5omk(!ox!z=-nrmh28m2y@ne1$)v=z_k'

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Amazon S3 requirements? 
os.environ['S3_USE_SIGV4'] = 'True'
os.environ['SWF'] = 'eu-central-1'

# AMAZON S3 STORAGE
AWS_STORAGE_BUCKET_NAME = 'yourin'
AWS_REGION = 'eu-central-1'
AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-central-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.contrib.wagtailroutablepage',

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'yourinuser',

    # Other third party apps
    'django_countries', # To populate country field of Address Model
    'rest_framework',   # API for calendar functionality
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'yourin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yourin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'nl-be'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#
#
# WAGTAIL SETTINGS
#
#
WAGTAIL_SITE_NAME = "yourin"


# Custom image model
WAGTAILIMAGES_IMAGE_MODEL = 'home.CustomImage'


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'

#
#
# TAGGIT SETTINGS
#
#

TAGGIT_TAGS_FROM_STRING = 'home.utils.comma_splitter' # Custom string to tag parser