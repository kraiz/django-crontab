from __future__ import print_function

import sys

from mock import Mock, patch

from nose.tools import assert_equal

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from django.conf import settings
from django.test.utils import override_settings

from django_crontab.crontab import Crontab


@patch('os.popen')
def test_read_crontab(mock_popen):
    """Test reading from the crontab."""
    mock_popen.return_value = Mock(
        stdout=StringIO(''),
        stderr=StringIO('crontab: no crontab for <user>')
    )

    crontab = Crontab()
    crontab.read()

    mock_popen.assert_called_with('/usr/bin/crontab -l')

@override_settings(CRONJOBS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')])
def test_add_jobs():
    crontab = Crontab()
    crontab.add_jobs()

    expected_crontab = ['*/5 * * * *  ' + sys.executable + ' ' + settings.CRONTAB_DJANGO_MANAGE_PATH + ' crontab run eb868be6b69c31faa6b03a4cf0dd3d8c   # django-cronjobs for tests\n']
    assert_equal(expected_crontab, crontab.crontab_lines)
