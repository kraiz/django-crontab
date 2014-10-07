from __future__ import print_function

import os
import subprocess

from django.core.management import call_command
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

    def _read_crontab(self):
        return os.popen('%s -l' % django_crontab.app_settings.CRONTAB_EXECUTABLE).readlines()

    @override_settings(CRONTABS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')])
    def test_single_format_1(self):
        self.assertTrue(True)
        print(self._read_crontab())
        call_command('crontab', ['add'])
        print(self._read_crontab())
        self.assertTrue(True)
