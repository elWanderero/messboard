"""
Django settings for messboard project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import django_heroku

from . import secret_settings

# SECURITY WARNING: keep the secret key used in production secret!
if hasattr(secret_settings, "SECRET_KEY"):
    SECRET_KEY: str = secret_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
if hasattr(secret_settings, "DEBUG"):
    DEBUG: bool = secret_settings.DEBUG


if hasattr(secret_settings, "ALLOWED_HOSTS"):
    ALLOWED_HOSTS: list = secret_settings.ALLOWED_HOSTS

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if hasattr(secret_settings, "DATABASES"):
    DATABASES = secret_settings.DATABASES

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = [
    "base.apps.BaseConfig",
    "api.apps.ApiConfig",
    "sajt.apps.SajtConfig",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "messboard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "messboard.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []  # DEV uncomment below in production
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
#     },
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "sv-SE"

TIME_ZONE = "Europe/Stockholm"  # "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}


# django.contrib.auth stuff

# Replace django auth's default User model. This is what get_user_model() calls
AUTH_USER_MODEL = "base.User"

# Allowed hashers. First in list is the main one used. The rest are used only
# for password verification, no new passwords are created with it. This is
# probably only necessary in a legacy system.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.BCryptSHA256PasswordHasher"]

LOGIN_REDIRECT_URL = "/sajt"


#############################
#           HEROKU          #
#############################

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Activate Django-Heroku.
django_heroku.settings(locals())
