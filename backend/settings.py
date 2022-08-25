"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
# import cloudinary
# import cloudinary_storage

if not os.environ.get('PRODUCTION'):
    from dotenv import load_dotenv
    load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_ROOT = BASE_DIR / 'static'

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR = Path(__file__).resolve().parent.parent
# STATIC_ROOT = BASE_DIR / 'static'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# FOR DEVELOPMENT ONLY
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['ycclav2.herokuapp.com', 'localhost:8000']

AUTH_USER_MODEL = "accounts.CustomUser"
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'accounts.backends.CaseInsensitiveModelBackend'
)
# Application definition

INSTALLED_APPS = [
    # MY APPS
    'accounts',
    'main_app',
    'test_kitchen',
    'cloudinary',
    'cloudinary_storage',
    'products',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ycclav2',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# HEROKU
# STATIC_ROOT = 'static_cdn'
# STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': str(os.getenv('CLOUD_NAME')),
#     'API_KEY': str(os.getenv('API_KEY')),
#     'API_SECRET': str(os.getenv('API_SECRET')),
# }

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloundinaryStorage'



STATIC_URL = '/static/'
# MEDIA_URL = '/media/'

# STATIC_ROOT = "static"
STATIC_ROOT = os.path.join(BASE_DIR, '../static') 

STATICFILES_DIRS = [
    # '../static'
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'media'),
]

# MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# TEMP = os.path.join(BASE_DIR, 'media_cdn/temp')

# if in production, use production URL
BASE_URL = "http://127.0.0.1:8000"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

# STRIPE INFORMATION
STRIPE_PUBLIC_KEY=str(os.getenv('STRIPE_PUBLIC_KEY'))
STRIPE_SECRET_KEY=str(os.getenv('STRIPE_SECRET_KEY'))
ENDPOINT_SECRET=str(os.getenv('ENDPOINT_SECRET'))
STRIPE_WEBHOOK_SECRET=""

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import django_heroku  
django_heroku.settings(locals())

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# sentry_sdk.init(
#     dsn="https://982487abd17f4a6c8f9d70fe3c0de60d@o1377629.ingest.sentry.io/6688515",
#     integrations=[
#         DjangoIntegration(),
#     ],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )
