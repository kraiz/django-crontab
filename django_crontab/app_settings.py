from django.conf import settings
from django.utils.importlib import import_module
import os
import re
import sys

# default app settings
# @see: http://www.muhuk.com/2010/01/developing-reusable-django-apps-app-settings/

CRONJOBS = getattr(settings, 'CRONJOBS', [])

CRONTAB_EXECUTABLE = getattr(settings, 'CRONTAB_EXECUTABLE', '/usr/bin/crontab')

CRONTAB_LINE_REGEXP = re.compile(r'^\s*(([^#\s]+\s+){5})([^#\n]*)\s*(#\s*([^\n]*)|$)')

CRONTAB_LINE_PATTERN = '%(time)s %(command)s # %(comment)s\n'

DJANGO_PROJECT_NAME = getattr(settings, 'CRONTAB_DJANGO_PROJECT_NAME', os.environ['DJANGO_SETTINGS_MODULE'].split('.')[0])

DJANGO_MANAGE_PATH = getattr(settings, 'CRONTAB_DJANGO_MANAGE_PATH', import_module(DJANGO_PROJECT_NAME + '.manage').__file__.replace('pyc', 'py'))

PYTHON_EXECUTABLE = getattr(settings, 'CRONTAB_PYTHON_EXECUTABLE', sys.executable)

CRONTAB_COMMENT = 'django-cronjobs for %s' % DJANGO_PROJECT_NAME

COMMAND_PREFIX = getattr(settings, 'CRONTAB_COMMAND_PREFIX', '')
COMMAND_SUFFIX = getattr(settings, 'CRONTAB_COMMAND_SUFFIX', '')
