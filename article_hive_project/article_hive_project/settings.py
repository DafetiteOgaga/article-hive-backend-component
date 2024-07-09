"""
Django settings for article_hive_project project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import configparser
import os

# config = configparser.ConfigParser()
# config.read('../emailBackend_config.cnf')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ks%dws4&%hgxe21a(9g+8dmp)9l(tq7k&w&s4cuz2=dy4joql^'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# ALLOWED_HOSTS = []

DEBUG = False # production
ALLOWED_HOSTS = [
    'dafetite.pythonanywhere.com',
    'localhost',
    '127.0.0.1'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'article_hive_app',		# <- added article_hive_app here
    # 'django_extensions',		# <- added django_extensions here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'article_hive_project.urls'

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

WSGI_APPLICATION = 'article_hive_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': '../MySQL_credentials.cnf',
#         },
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Added static variable here
STATICFILES_DIRS = [
    BASE_DIR / 'static',		# <- added static to BASE_DIR
    BASE_DIR / 'static/article_hive_project',		# <- added static to project dir.
]

# custom user model
AUTH_USER_MODEL = 'article_hive_app.User'

# login redirect for anonymous users
LOGIN_URL = '/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('email_host')
# EMAIL_PORT = os.environ.get('email_port')
# EMAIL_HOST_USER = os.environ.get('email_user')
# EMAIL_HOST_PASSWORD = os.environ.get('email_password')
# DEFAULT_FROM_EMAIL = os.environ.get('email_default_from')
# EMAIL_USE_TLS = True
# or
# EMAIL_HOST = config.get('email', 'host')
# EMAIL_PORT = config.getint('email', 'port')
# EMAIL_HOST_USER = config.get('email', 'user')
# EMAIL_HOST_PASSWORD = config.get('email', 'password')
# EMAIL_USE_TLS = config.getboolean('email', 'use_tls')
# DEFAULT_FROM_EMAIL = config.get('email', 'default_from')

# # urls for password reset
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = 'home'

# Media files custom added
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

##########
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # For collectstatic
# STATICFILES_DIRS = [BASE_DIR / 'static']

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
##########
