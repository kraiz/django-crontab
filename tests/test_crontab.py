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
        stdout=StringIO(u''),
        stderr=StringIO(u'crontab: no crontab for <user>')
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

@override_settings(CRONJOBS=[('*/1 * * * *', 'tests.cron.cron_job')])
@patch('tests.cron.cron_job')
def test_run_no_arg_format1_job(method_to_call):
    crontab = Crontab()
    crontab.run_job('4f30993ab69a8c5763ce55f762ef0433')
    method_to_call.assert_called_with()

@override_settings(CRONJOBS=[('*/1 * * * *', 'tests.cron.cron_job', '> /home/myhome/logs/cron_job.log')])
@patch('tests.cron.cron_job')
def test_run_no_arg_format1_job_with_suffix(method_to_call):
    crontab = Crontab()
    crontab.run_job('53e6fe5b66bd870e396d574ba1503c33')
    method_to_call.assert_called_with()

@override_settings(CRONJOBS=[('*/1 * * * *', 'tests.cron.cron_job', [1, 'two'])])
@patch('tests.cron.cron_job')
def test_run_args_only_format2_job(method_to_call):
    crontab = Crontab()
    crontab.run_job('369f8418b0f8cf1fff78c547516aa8e0')
    method_to_call.assert_called_with(1, 'two')

@override_settings(CRONJOBS=[('*/1 * * * *', 'tests.cron.cron_job', [1, 'two'], {'test': 34, 'a': 's2'})])
@patch('tests.cron.cron_job')
def test_run_format2_job(method_to_call):
    crontab = Crontab()
    crontab.run_job('13e8169dffe273b8b0c5f8abe1b6f643')
    method_to_call.assert_called_with(1, 'two', test=34, a='s2')

@override_settings(CRONJOBS=[('*/1 * * * *', 'tests.cron.cron_job', [1, 'two'], dict(), 'some suffix')])
@patch('tests.cron.cron_job')
def test_run_args_only_format2_job(method_to_call):
    crontab = Crontab()
    crontab.run_job('fefa68aed4ff509331ee6a5b62ea5e5c')
    method_to_call.assert_called_with(1, 'two')

