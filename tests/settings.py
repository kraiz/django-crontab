# Django settings for test_project project.
import os

DEBUG = True

INSTALLED_APPS = (
    'django_crontab',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

MIDDLEWARE_CLASSES = ()

SECRET_KEY = 'not-so-secret'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django_crontab': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

CRONTAB_DJANGO_MANAGE_PATH = os.path.join(os.path.dirname(__file__), '', 'test_manage.py')
