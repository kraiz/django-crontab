from __future__ import print_function

from mock import Mock, patch

from StringIO import StringIO

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from django_crontab.crontab import Crontab


class CrontabTestCase(TestCase):

    @patch('os.popen')
    def test_read_crontab(self, mock_popen):
        """Test reading from the crontab."""
        mock_popen.return_value = Mock(
            stdout=StringIO(''),
            stderr=StringIO('crontab: no crontab for <user>')
        )

        crontab = Crontab()
        crontab.read()

        mock_popen.assert_called_with('/usr/bin/crontab -l')

    @override_settings(CRONJOBS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')])
    def test_add_jobs(self):
        crontab = Crontab()
        crontab.add_jobs()

        expected_crontab = ['*/5 * * * *  /usr/bin/python ' + settings.CRONTAB_DJANGO_MANAGE_PATH + ' crontab run eb868be6b69c31faa6b03a4cf0dd3d8c   # django-cronjobs for django_crontab\n']
        self.assertEqual(expected_crontab, crontab.crontab_lines)
