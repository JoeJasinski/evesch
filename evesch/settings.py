# Django settings for evesch project.
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
ENVIRONMENT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', '..'))
HTDOCS_ROOT = os.path.abspath(os.path.join(ENVIRONMENT_ROOT, 'htdocs'))
LOG_ROOT = os.path.abspath(os.path.join(ENVIRONMENT_ROOT, 'var', 'log'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "core"))

DEBUG = True

ADMINS = (
    # ('joe', 'joe@evesch.com'),
)

MANAGERS = ADMINS
AUTH_USER_MODEL = 'euser.eUser'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_BACKEND', 'django.db.backends.postgresql_psycopg2'), # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.getenv('DATABASE_NAME', 'postgres'),
        # The following settings are not used with sqlite3:
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'postgres'),
        'HOST': os.getenv('DATABASE_HOST', 'db'),
        'PORT':  os.getenv('DATABASE_PORT', '5432'),
    }
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

INTERNAL_IPS = ('127.0.0.1', 'localhost',)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = os.path.abspath(os.path.join(HTDOCS_ROOT, 'media'))
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(HTDOCS_ROOT, 'static') 

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    'dummy-value-change-me')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'pagination.middleware.PaginationMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
    # 'evesch.core.middleware.StripWhitespaceMiddleware.StripWhitespaceMiddleware',
    # 'evesch.core.middleware.threadlocals.ThreadLocals',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'evesch.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'evesch.wsgi.application'


TEMPLATES = [
    {
        "BACKEND": 'django.template.backends.django.DjangoTemplates',
        "DIRS": [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',
                'django.template.context_processors.debug',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rosetta',   # used for easily editing i18n files
    'pagination_bootstrap',
    'django_extensions',

    'evesch.core',
    'evesch.org',
    'evesch.org.avatar',
    'evesch.egroup',
    'evesch.euser',
    'evesch.event',
    'evesch.ecalendar',
    'evesch.core.feed',
#    'core.debug_toolbar',  # adds debug toolbar that shows various stats
    'evesch.core.ajax_filtered_fields', 
    'evesch.report',
    'evesch.post',
)

# max size for profie photo uploads (in KB)
MAX_PHOTO_UPLOAD_SIZE = 2000

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'evesch': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


TEST_RUNNER = 'evesch.runner.PytestTestRunner'
