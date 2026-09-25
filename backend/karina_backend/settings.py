import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# Search for .env in BASE_DIR, parent directory, and current working directory
for candidate_env in [BASE_DIR / '.env', BASE_DIR.parent / '.env', Path.cwd() / '.env']:
    if candidate_env.exists():
        load_dotenv(candidate_env, override=False)

DEBUG = os.getenv('DEBUG', 'True') == 'True'

SECRET_KEY = os.getenv('SECRET_KEY') or os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    # Fallback to robust key so production containers and Gunicorn never crash on startup
    SECRET_KEY = 'Z_FXf1s1KAksWSMqd-zaAhdPmYvRHxkQ5QlQtmxsyA5EJfmJdTHtLJ3aBEeGKqAVmP8'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'storages',
    
    # Local apps
    'booking_api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'karina_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

import dj_database_url

WSGI_APPLICATION = 'karina_backend.wsgi.application'

# Unified PostgreSQL Engine (Supabase Transaction Pooler)
_db_port = os.getenv('DB_PORT', '5432')
_is_pooler = 'pooler.supabase.com' in os.getenv('DB_HOST', '') or _db_port == '6543'
_default_conn_max_age = '0' if _is_pooler else '60'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': _db_port,
        'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', _default_conn_max_age)),
    }
}

# Supabase S3 Media Storage Configuration
AWS_ACCESS_KEY_ID = os.getenv('SUPABASE_STORAGE_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('SUPABASE_STORAGE_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('SUPABASE_STORAGE_BUCKET_NAME', 'Booking_public')
AWS_S3_ENDPOINT_URL = os.getenv('SUPABASE_STORAGE_ENDPOINT_URL')
AWS_S3_REGION_NAME = os.getenv('SUPABASE_STORAGE_REGION', 'eu-west-1')
AWS_S3_CUSTOM_DOMAIN = os.getenv('SUPABASE_STORAGE_CUSTOM_DOMAIN')
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_S3_ENDPOINT_URL:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "endpoint_url": AWS_S3_ENDPOINT_URL,
                "region_name": AWS_S3_REGION_NAME,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "file_overwrite": False,
                "querystring_auth": False,
                "default_acl": None,
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/" if AWS_S3_CUSTOM_DOMAIN else f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB for high-resolution studio photography
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# REST Framework - Exclusively Simple JWT Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'

import sys
if 'test' in sys.argv:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True


# Simple JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}