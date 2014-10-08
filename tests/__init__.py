import os

from django.test.utils import setup_test_environment


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
setup_test_environment()
