import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables")

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
# Using .lower() to make it case-insensitive

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS is not set in the environment variables")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'social_django',
    'accounts',
    'drf_yasg',
    'ai',
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}

# SECRET_KEY = os.getenv('SECRET_KEY')
# if not SECRET_KEY:
#     raise ValueError("SECRET_KEY is not set in the environment variables")

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', os.getenv('SECRET_KEY')),  # Fallback to SECRET_KEY
}

CORS_ALLOW_ALL_ORIGINS = True  # Adjust for production

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', 'adlm_skillhub'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'postgres'),  # Use env variable
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')  # Default to Gmail
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
if not EMAIL_HOST_USER:
    raise ValueError("EMAIL_HOST_USER is not set in the environment variables")
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
if not EMAIL_HOST_PASSWORD:
    raise ValueError("EMAIL_HOST_PASSWORD is not set in the environment variables")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = os.getenv('LINKEDIN_CLIENT_ID')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Ensure this is present
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL = 'accounts.User'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

ROOT_URLCONF = 'core.urls'



TEST_DISCOVER_TOP_LEVEL = True

# Test settings
# TESTS_DIR = [
#     os.path.join(BASE_DIR, 'accounts/tests'),
#     os.path.join(BASE_DIR, 'ai/tests'),
# ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}