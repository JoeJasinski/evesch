from evesch.base_settings import * 

DEBUG=True
COMPRESS_ENABLED = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(ENVIRONMENT_ROOT, 'data', 'evesch.db'),
        # The following settings are not used with sqlite3:
        'USER': 'evesch',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}