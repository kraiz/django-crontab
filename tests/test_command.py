from unittest.mock import patch

from django.core.management import CommandError, call_command
from django.test import SimpleTestCase

from django_crontab.crontab import Crontab


class CrontabCommandTest(SimpleTestCase):

    @patch.object(Crontab, 'add_jobs')
    @patch.object(Crontab, 'remove_jobs')
    @patch.object(Crontab, 'run_job')
    def test_add_command(self, run_mock, remove_mock, add_mock):
        call_command('crontab', 'add')
        self.assertTrue(remove_mock.called)
        self.assertTrue(add_mock.called)
        self.assertFalse(run_mock.called)

    @patch.object(Crontab, 'add_jobs')
    @patch.object(Crontab, 'remove_jobs')
    @patch.object(Crontab, 'run_job')
    def test_remove_command(self, run_mock, remove_mock, add_mock):
        call_command('crontab', 'remove')
        self.assertTrue(remove_mock.called)
        self.assertFalse(add_mock.called)
        self.assertFalse(run_mock.called)

    @patch.object(Crontab, 'add_jobs')
    @patch.object(Crontab, 'remove_jobs')
    @patch.object(Crontab, 'run_job')
    def test_run_command(self, run_mock, remove_mock, add_mock):
        call_command('crontab', 'run', 'abc123')
        self.assertFalse(remove_mock.called)
        self.assertFalse(add_mock.called)
        run_mock.assert_called_once_with('abc123')

    @patch.object(Crontab, 'add_jobs')
    @patch.object(Crontab, 'remove_jobs')
    @patch.object(Crontab, 'run_job')
    @patch.object(Crontab, 'show_jobs')
    def test_show_command(self, show_mock, run_mock, remove_mock, add_mock):
        call_command('crontab', 'show')
        self.assertFalse(remove_mock.called)
        self.assertFalse(add_mock.called)
        self.assertFalse(run_mock.called)
        self.assertTrue(show_mock.called)

    @patch.object(Crontab, 'add_jobs')
    @patch.object(Crontab, 'remove_jobs')
    @patch.object(Crontab, 'run_job')
    @patch.object(Crontab, 'show_jobs')
    def test_help_command(self, show_mock, run_mock, remove_mock, add_mock):
        with self.assertRaises(CommandError):
            call_command('crontab', help=True)
        self.assertFalse(remove_mock.called)
        self.assertFalse(add_mock.called)
        self.assertFalse(run_mock.called)
        self.assertFalse(show_mock.called)
