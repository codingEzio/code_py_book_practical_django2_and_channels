import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nl*^o7w$go+uia-tyxfok7om6$12k(=ucrt3j+-2sfl)hmbbr2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Normally the order isn't necessary here.
#   BUT, it DOES make a different for the 'channels' app.
#   It overrides the `runserver` command of standard Django.
INSTALLED_APPS = [
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main.apps.MainConfig',

    "webpack_loader",
    "django_extensions",
    "debug_toolbar",
    "django_tables2",
    "django_filters",
    "widget_tweaks",

    "rest_framework",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # user-related
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # user-related
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "main.middlewares.basket_middleware",
]

ROOT_URLCONF = 'booktime.urls'

TEMPLATES = [
    {
        # This default configuration will try to
        # find 'templates' folders in each respective apps. (aka. APP_DIRS)
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

WSGI_APPLICATION = 'booktime.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'projbooktime',
        'USER': 'projbooktimeuser',
        'PASSWORD': 'whatever',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_TZ = True

USE_I18N = True
USE_L10N = True

# While in production mode, the 'static' files
#   should be served by a efficient HTTP server like Nginx.
#   There's also a constant for it: `STATIC_ROOT` (specifying dir).
STATIC_URL = '/static/'

# This one is quite different from "STATIC_XXX"
#   this one is specifically for storing "user-generated" content.
#   Still, you should use a real server to "serve" the media stuff.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

if DEBUG:
    # This would send mails to our consoles :P
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    # I'll configure this when it's needed
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.what-is-it.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = "who-is-it"
    EMAIL_HOST_PASSWORD = "what-is-it"

# Logging
#   internal: using build-in 'logging' module
#   doc-site: https://docs.djangoproject.com/en/2.1/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },

    'loggers': {
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'booktime': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Customizing 'User' model
AUTH_USER_MODEL = "main.user"

# Redirect to WHERE
LOGIN_REDIRECT_URL = "/"

# Webpack related (bundler)
WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "bundles/",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
    }
}

# Related config of 'django-debug-toolbar'
INTERNAL_IPS = ["127.0.0.1"]

# Configuration of Django REST Framework ( aka. DRF )
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.DjangoModelPermissions",
    ),
    "DEFAULT_FILTER_CLASSES": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination",
    ),
    "PAGE_SIZE": 100,
}

# Configuration for 'Django Channels' (async-related)
#   Some preliminary steps for this
#   1. brew install redis && redis-server
#   2. pipenv install channels
#   3. pipenv install channels_redis
#   4. 'routing.py' under PROJECT folder (same level as 'settings.py')
ASGI_APPLICATION = "booktime.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        }
    }
}
