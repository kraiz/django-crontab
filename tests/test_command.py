from __future__ import print_function

from mock import patch

from django.core.management import call_command

from django_crontab.crontab import Crontab



@patch.object(Crontab, 'add_jobs')
@patch.object(Crontab, 'remove_jobs')
@patch.object(Crontab, 'run_job')
def test_add_command(run_mock, remove_mock, add_mock):
    call_command('crontab', 'add')
    assert remove_mock.called
    assert add_mock.called
    assert not run_mock.called


@patch.object(Crontab, 'add_jobs')
@patch.object(Crontab, 'remove_jobs')
@patch.object(Crontab, 'run_job')
def test_remove_command(run_mock, remove_mock, add_mock):
    print(add_mock)
    call_command('crontab', 'remove')
    assert remove_mock.called
    assert not add_mock.called
    assert not run_mock.called


@patch.object(Crontab, 'add_jobs')
@patch.object(Crontab, 'remove_jobs')
@patch.object(Crontab, 'run_job')
def test_run_command(run_mock, remove_mock, add_mock):
    call_command('crontab', 'run', 'abc123')
    assert not remove_mock.called
    assert not add_mock.called
    run_mock.assert_called_once_with('abc123')


@patch.object(Crontab, 'add_jobs')
@patch.object(Crontab, 'remove_jobs')
@patch.object(Crontab, 'run_job')
@patch.object(Crontab, 'show_jobs')
def test_show_command(show_mock, run_mock, remove_mock, add_mock):
    call_command('crontab', 'show')
    assert not remove_mock.called
    assert not add_mock.called
    assert not run_mock.called
    assert show_mock.called


@patch.object(Crontab, 'add_jobs')
@patch.object(Crontab, 'remove_jobs')
@patch.object(Crontab, 'run_job')
@patch.object(Crontab, 'show_jobs')
def test_show_command(show_mock, run_mock, remove_mock, add_mock):
    call_command('crontab', 'help')
    assert not remove_mock.called
    assert not add_mock.called
    assert not run_mock.called
    assert not show_mock.called

