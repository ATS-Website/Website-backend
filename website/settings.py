"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from decouple import config
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY")
QR_SECRET_KEY = config("QR_SECRET_KEY")
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = decouple.config("DEBUG", cast=bool)

# SECRET_KEY = "django-insecure-ep&9526=*1u9%r(rcke7qf&wt&__)ak$*94p-h7h0&gs(b)emd"
DEBUG = True
# DEBUG = config("DEBUG", cast=bool, default=True)
# ADMIN = config("ADMIN")


# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['atsbk.afexats.com', '127.0.0.1', 'localhost', 'localhost:3000',
                 '127.0.0.1:3000', 'localhost:8000', '127.0.0.1:8000', ]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # internal apps
    "Accounts",
    "Blogs",
    "Support",
    "Tech_Stars",
    # thirdparty services
    "rest_framework",
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    # external api
    'algoliasearch_django',
    'django_celery_results',
    "djcelery_email",
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    # 'django-celery-beat',
    # "cloudinary_storage",
    # 'cloudinary',

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
    "Tech_Stars.middleware.EncryptionAndDecryptionMiddleware",

]

ROOT_URLCONF = 'website.urls'
CORS_ALLOWED_ORIGINS = ['https://6384b950f2c6e80009106d70--zippy-dango-7ea3fe.netlify.app',
                        'http://localhost:3000', 'http://127.0.0.1:3000']
CORS_ALLOW_CREDENTIALS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config("DB_NAME"),
#         'USER': config("DB_USER"),
#         'PASSWORD': config("DB_PASSWORD"),
#         'PORT': config("DB_PORT"),
#         'HOST': config("DB_HOST"),
#
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "Website",
        'USER': "postgres",
        'PASSWORD': 'root',
        'PORT': '5432',
        'HOST': 'localhost',

    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIR = [STATIC_ROOT, ]

# STATICFILES_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = "media/"
# DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "Accounts.Account"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'Accounts.permissions.IsValidRequestAPIKey',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        'Accounts.renderers.CustomRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=2000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
}

ALGOLIA = {
    'APPLICATION_ID': config('ALG_APPLICATION_ID'),
    'API_KEY': config('ALG_API_KEY'),
    'INDEX_PREFIX': 'ats',
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://127.0.0.1:9200'
    },
}

ELASTICSEARCH_INDEX_NAMES = {
    'Blogs.NewsArticle': 'news',
    'Blogs.BlogArticle': 'blogs',
    'Tech_Stars.Tech_Star': "techstars"
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", cast=int)

# CELERY

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_TIMEZONE = "AFrica/Lagos"
CELERY_ACCEPT_CONTENT = ["application/json"]
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# CLOUDINARY_STORAGE = {
#     "CLOUD_NAME": config("CLOUD_NAME"),
#     "API_KEY": config("CLOUD_API_KEY"),
#     "API_SECRET": config("CLOUD_API_SECRET"),
#     'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr',
#                                  'hdp', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff', 'ico'],

# }

# CELERY-BEAT
CELERY_BEAT_SCHEDULER = 'djanga_celery_beat.schedulers:DatabaseScheduler'
