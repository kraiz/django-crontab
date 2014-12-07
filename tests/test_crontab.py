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


@override_settings(CRONJOBS=[('*/1 * * * *', 'tests.cron.cron_job')])
@patch('os.popen')
@patch('os.system')
def test_read_write_crontab(mock_system, mock_popen):
    def crontab_write_mock(cmd):
        executable, tmp_file = cmd.split()
        assert_equal(executable, '/usr/bin/crontab')
        with open(tmp_file, 'r') as f:
            assert_equal(
                ['@reboot /existing/command --with=2 params\n', '1 2 3 4 5 /new/command > /var/log/cmd.log\n'],
                f.readlines()
            )
        return ''

    mock_popen.return_value = StringIO(u'@reboot /existing/command --with=2 params\n')
    mock_system.side_effect = crontab_write_mock
    with Crontab() as crontab:
        mock_popen.assert_called_with('/usr/bin/crontab -l')
        assert_equal(['@reboot /existing/command --with=2 params\n'], crontab.crontab_lines)
        crontab.crontab_lines.append('1 2 3 4 5 /new/command > /var/log/cmd.log\n')

    mock_system.assert_called_once()


@override_settings(CRONJOBS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')])
def test_add_single_simple_job():
    crontab = Crontab()
    crontab.add_jobs()
    expected_line = ['*/5 * * * * %(exe)s %(manage)s crontab run eb868be6b69c31faa6b03a4cf0dd3d8c # django-cronjobs for tests\n' % {
        'exe': sys.executable,
        'manage': settings.CRONTAB_DJANGO_MANAGE_PATH
    }]
    assert_equal(expected_line, crontab.crontab_lines)


@override_settings(CRONJOBS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')], CRONTAB_DJANGO_SETTINGS_MODULE='myproj.other_settings')
def test_add_job_with_settings():
    crontab = Crontab()
    crontab.add_jobs()
    expected_line = ['*/5 * * * * %(exe)s %(manage)s crontab run eb868be6b69c31faa6b03a4cf0dd3d8c --settings=myproj.other_settings # django-cronjobs for tests\n' % {
        'exe': sys.executable,
        'manage': settings.CRONTAB_DJANGO_MANAGE_PATH
    }]
    assert_equal(expected_line, crontab.crontab_lines)


@override_settings(CRONJOBS=[
    ('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job'),
    ('* 3 * * *', 'tests.cron.cron_job', '> /home/myhome/logs/cron_job.log'),
    ('0 4 * * *', 'tests.cron.cron_job', [1, 'two'], {'test': 34, 'a': 's2'}),
    ('1 2 */5 * 0', 'tests.cron.cron_job', [1, 'two'], {'test': 34, 'a': 's2'}, 'suffix'),
])
def test_add_many_different_jobs():
    crontab = Crontab()
    crontab.add_jobs()
    ctx = dict(exe=sys.executable, manage=settings.CRONTAB_DJANGO_MANAGE_PATH)
    expected_lines = [
        '*/5 * * * * %(exe)s %(manage)s crontab run eb868be6b69c31faa6b03a4cf0dd3d8c # django-cronjobs for tests\n' % ctx,
        '* 3 * * * %(exe)s %(manage)s crontab run c03a5151588fde26da760240ed6a9b9a > /home/myhome/logs/cron_job.log # django-cronjobs for tests\n' % ctx,
        '0 4 * * * %(exe)s %(manage)s crontab run e5b6fc0d28edb93283faf23e808b1065 # django-cronjobs for tests\n' % ctx,
        '1 2 */5 * 0 %(exe)s %(manage)s crontab run e1d364332622aa2c382fcb325a5b388a suffix # django-cronjobs for tests\n' % ctx,
    ]
    assert_equal(len(expected_lines), len(crontab.crontab_lines))
    for expected, actual in zip(expected_lines, crontab.crontab_lines):
        assert_equal(expected, actual)


@override_settings(CRONJOBS=[
    ('*/1 * * * *', 'tests.cron.cron_job'),
    ('1 2 */5 * 0', 'tests.cron.cron_job', [1, 'two'], {'test': 34}, 'suffix'),
])
def test_show_jobs():
    crontab = Crontab()
    crontab.add_jobs()

    stdout = sys.stdout
    try:
        sys.stdout = StringIO()
        crontab.show_jobs()
        assert_equal(
            "Currently active jobs in crontab:\n"
            "4f30993ab69a8c5763ce55f762ef0433 -> ('*/1 * * * *', 'tests.cron.cron_job')\n"
            "95f7703a7d571917dda67f8bd294868a -> ('1 2 */5 * 0', 'tests.cron.cron_job', [1, 'two'], {'test': 34}, 'suffix')\n",
            sys.stdout.getvalue()
        )
    finally:
        sys.stdout = stdout


@override_settings(CRONJOBS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')])
def test_remove_single_simple_job():
    crontab = Crontab()
    crontab.crontab_lines = ['*/5 * * * *  %(exe)s %(manage)s crontab run eb868be6b69c31faa6b03a4cf0dd3d8c   # django-cronjobs for tests\n' % {
        'exe': sys.executable,
        'manage': settings.CRONTAB_DJANGO_MANAGE_PATH
    }]
    crontab.remove_jobs()
    assert_equal([], crontab.crontab_lines)


@override_settings(CRONJOBS=[
    ('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job'),
    ('* 3 * * *', 'tests.cron.cron_job', '> /home/myhome/logs/cron_job.log'),
    ('0 4 * * *', 'tests.cron.cron_job', [1, 'two'], {'test': 34, 'a': 's2'}),
    ('1 2 */5 * 0', 'tests.cron.cron_job', [1, 'two'], {'test': 34, 'a': 's2'}, 'suffix'),
])
def test_remove_many_different_jobs():
    crontab = Crontab()
    ctx = dict(exe=sys.executable, manage=settings.CRONTAB_DJANGO_MANAGE_PATH)
    crontab.crontab_lines = [
        '*/5 * * * *  %(exe)s %(manage)s crontab run eb868be6b69c31faa6b03a4cf0dd3d8c   # django-cronjobs for tests\n' % ctx,
        '* 3 * * *  %(exe)s %(manage)s crontab run c03a5151588fde26da760240ed6a9b9a > /home/myhome/logs/cron_job.log  # django-cronjobs for tests\n' % ctx,
        '0 4 * * *  %(exe)s %(manage)s crontab run e5b6fc0d28edb93283faf23e808b1065   # django-cronjobs for tests\n' % ctx,
    ]
    crontab.remove_jobs()
    assert_equal([], crontab.crontab_lines)


@override_settings(CRONJOBS=[('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')])
def test_remove_job_but_keep_anything_else():
    crontab = Crontab()
    ctx = dict(exe=sys.executable, manage=settings.CRONTAB_DJANGO_MANAGE_PATH)
    crontab.crontab_lines = [
        'MAIL=john@doe.org',
        '*/5 * * * *  %(exe)s %(manage)s crontab run eb868be6b69c31faa6b03a4cf0dd3d8c   # django-cronjobs for tests\n' % ctx,
        '* * * * * /some/other/job that --has=nothing > /to/do.with # us'
    ]
    crontab.remove_jobs()
    assert_equal([
        'MAIL=john@doe.org',
        '* * * * * /some/other/job that --has=nothing > /to/do.with # us'
    ], crontab.crontab_lines)


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

