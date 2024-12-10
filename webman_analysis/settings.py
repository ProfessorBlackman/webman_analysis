import os
from datetime import timedelta
from pathlib import Path

from decouple import config

from webman_analysis.custom_logging import DefaultJsonFormatter, DetailedJsonFormatter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config("DEBUG")

ALLOWED_HOSTS = ["*"]

# Cors configuration
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_yasg',
    # local apps
    'authentication.apps.AuthenticationConfig'
]

AUTH_USER_MODEL = 'authentication.User'
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "django.middleware.gzip.GZipMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
    'django.middleware.common.BrokenLinkEmailsMiddleware'
]

ROOT_URLCONF = 'webman_analysis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'webman_analysis.wsgi.application'

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    },
}

# Redis configuration
REDIS_CONFIG = {
    "host": config("REDIS_HOST_URL"),
    "port": config("REDIS_PORT", default=6379, cast=int),
    "db": 0,
}

# Email configurations
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT")

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration

LOG_FILES_DIR = BASE_DIR / "logs"


def create_path(file_name: str):
    # Create the logs directory if it does not exist
    if not LOG_FILES_DIR.exists():
        LOG_FILES_DIR.mkdir(parents=True)
    return LOG_FILES_DIR / file_name


log_files = {
    "wma_main": create_path("main.log"),
    "wma_auth": create_path("auth.log"),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": config("LOG_LEVEL", default="INFO"),
        "handlers": ["console", "wma_main"],
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "default_json": {"()": DefaultJsonFormatter},
        "detailed_json": {"()": DetailedJsonFormatter}
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "wma_main": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_files["wma_main"],
            "formatter": "default_json",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
        },
        "wma_auth": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_files["wma_auth"],
            "formatter": "default_json",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "main": {
            "handlers": ["console", "wma_main"],
            "level": "INFO",
            "propagate": False,
        },
        "auth": {
            "handlers": ["console", "wma_auth"],
            "level": "INFO",
            "propagate": False,
        },
    }
}
