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
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = decouple.config("DEBUG", cast=bool)

# SECRET_KEY = "django-insecure-ep&9526=*1u9%r(rcke7qf&wt&__)ak$*94p-h7h0&gs(b)emd"
DEBUG = True
# DEBUG = config("DEBUG", cast=bool, default=True)


ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = [
#     'localhost',
#     '127.0.0.1',
#     '111.222.333.444',
#     'mywebsite.example']

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
    # external api
    'algoliasearch_django',
    "cloudinary_storage",
    'cloudinary',
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

ROOT_URLCONF = 'website.urls'

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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Website',
        'USER': 'postgres',
        'PASSWORD': config('DB_PASSWORD'),
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
STATICFILES_DIR = os.path.join(BASE_DIR, "static")
# STATIC_URL = '/static/'
# STATICFILES_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = "media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "Accounts.Account"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',  # new
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # new
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ),
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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", cast=int)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUD_NAME"),
    "API_KEY": config("CLOUD_API_KEY"),
    "API_SECRET": config("CLOUD_API_SECRET"),
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr',
                                 'hdp', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff', 'ico'],
    'STATIC_VIDEOS_EXTENSIONS': ['mp4', 'webm', 'flv', 'mov', 'ogv', '3gp', '3g2', 'wmv',
                                 'mpeg', 'flv', 'mkv', 'avi'],
}
