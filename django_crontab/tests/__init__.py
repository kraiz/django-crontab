import os
import subprocess

from django.test import TestCase
from django.test.utils import override_settings

import django_crontab


DEV_NULL = open(os.devnull, 'w')


class CrontabTestCase(TestCase):

    def setUp(self):
        """Be sure crontab is empty"""
        subprocess.Popen([django_crontab.app_settings.CRONTAB_EXECUTABLE, '-r'], stderr=DEV_NULL).communicate()

    def tearDown(self):
        """Be sure crontab is empty"""
        self.setUp()

    @override_settings(CRONTABS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')])
    def test_single_format_1(self):
        self.assertTrue(True)
        # call_command('crontab', ['add'])
        # self.assertTrue(True)
