"""
Django settings for elizabethandgeorge project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
ENVIRONMENT = os.environ['ENVIRONMENT']

if ENVIRONMENT == 'production':
    from elizabethandgeorge.settings_production import private_ip

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


if ENVIRONMENT == 'local':
    ALLOWED_HOSTS = ['localhost','9536-41-90-69-123.ngrok-free.app']
elif ENVIRONMENT == 'production':
    ALLOWED_HOSTS = ['prod-env.eba-fc7hmtbi.eu-west-1.elasticbeanstalk.com','172.31.16.5','elizabethgeorge.zitto.co.ke',private_ip]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "gifts",
    "storages"
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

ROOT_URLCONF = "elizabethandgeorge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/"templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "elizabethandgeorge.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME'), 
            'USER': os.environ.get('DB_USERNAME'), 
            'PASSWORD': os.environ.get('DB_PASSWORD'), 
            'HOST': os.environ.get('DB_ENDPOINT'), 
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




##Pesapal integration
PESAPAL_AUTHENTICATION_URL = os.environ['PEASAPAL_AUTHENTICATION_URL']
PESAPAL_CONSUMER_KEY = os.environ['PESAPAL_CONSUMER_KEY']
PESAPAL_CONSUMER_SECRET = os.environ['PESAPAL_CONSUMER_SECRET']
PESAPAL_ORDER_REQUEST_URL = os.environ['PESAPAL_ORDER_REQUEST_URL']
PESAPAL_IPN_REGISTRATION_URL = os.environ['PESAPAL_IPN_REGISTRATION_URL']
PESAPAL_GET_TRANSACTION_STATUS_URL = os.environ['PESAPAL_GET_TRANSACTION_STATUS_URL']
PESAPAL_REDIRECT_URL = os.environ['PESAPAL_REDIRECT_URL']
PESAPAL_RESPONSE_URL = os.environ['PESAPAL_RESPONSE_URL']

#Mpesa credentials
MPESA_CONSUMER_KEY = os.environ['MPESA_CONSUMER_KEY']
MPESA_CONSUMER_SECRET = os.environ['MPESA_CONSUMER_SECRET']
MPESA_BUSINESS_SHORT_CODE = os.environ['MPESA_BUSINESS_SHORT_CODE']
MPESA_LIPA_NA_MPESA_PASSKEY = os.environ['MPESA_LIPA_NA_MPESA_PASSKEY']
MPESA_CALL_BACK_URL = os.environ['MPESA_CALL_BACK_URL']

MPESA_ACCESS_TOKEN_API_URL = os.environ['MPESA_ACCESS_TOKEN_API_URL']
MPESA_PROCESS_REQUEST_API_URL = os.environ['MPESA_PROCESS_REQUEST_API_URL']
MPESA_B2C_PROXY_URL = os.environ['MPESA_B2C_PROXY_URL']
MPESA_TRANSACTION_DESC = os.environ['MPESA_TRANSACTION_DESC']


#s3 sTATIC STORAGE
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).

if ENVIRONMENT == 'production':
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


SUPERUSER_USERNAME = os.environ['SUPERUSER_USERNAME']
SUPERUSER_EMAIL = os.environ['SUPERUSER_EMAIL']
SUPERUSER_PASSWORD = os.environ['SUPERUSER_PASSWORD']