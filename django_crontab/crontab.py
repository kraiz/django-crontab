from __future__ import print_function

import fcntl
import hashlib
import json
import logging
import os
import tempfile

from django.conf import settings

from django.utils.importlib import import_module

from django_crontab.app_settings import Settings

logger = logging.getLogger(__name__)


class Crontab(object):

    def __init__(self, **options):
        self.verbosity = options.get('verbosity', 1)
        self.readonly = options.get('readonly', False)
        self.crontab_lines = []
        self.settings = Settings(settings)

    def __enter__(self):
        """
        Automatically read crontab when used as with statement
        """
        self.read()
        return self

    def __exit__(self, type, value, traceback):
        """
        Automatically write back crontab when used as with statement if readonly is False
        """
        if not self.readonly:
            self.write()

    def read(self):
        """
        Reads the crontab into internal buffer
        """
        self.crontab_lines = os.popen('%s -l' % self.settings.CRONTAB_EXECUTABLE).readlines()

    def write(self):
        """
        Writes internal buffer back to crontab
        """
        fd, path = tempfile.mkstemp()
        tmp = os.fdopen(fd, 'w')
        for line in self.crontab_lines:
            tmp.write(line)
        tmp.close()
        os.system('%s %s' % (self.settings.CRONTAB_EXECUTABLE, path))
        os.unlink(path)

    def add_jobs(self):
        """
        Adds all jobs defined in CRONJOBS setting to internal buffer
        """
        for job in self.settings.CRONJOBS:
            # differ format and find job's suffix
            if len(job) > 2 and isinstance(job[2], (basestring, unicode)):
                # format 1 job
                job_suffix = job[2]
            elif len(job) > 4:
                job_suffix = job[4]
            else:
                job_suffix = ''

            self.crontab_lines.append(self.settings.CRONTAB_LINE_PATTERN % {
                'time': job[0],
                'comment': self.settings.CRONTAB_COMMENT,
                'command': (
                    '%(global_prefix)s %(exec)s %(manage)s crontab run '
                    '%(jobname)s %(job_suffix)s %(global_suffix)s'
                ) % {
                    'global_prefix': self.settings.COMMAND_PREFIX,
                    'exec': self.settings.PYTHON_EXECUTABLE,
                    'manage': self.settings.DJANGO_MANAGE_PATH,
                    'jobname': self.__hash_job(job),
                    'job_suffix': job_suffix,
                    'global_suffix': self.settings.COMMAND_SUFFIX
                }
            })
            if self.verbosity >= 1:
                print('  adding cronjob: (%s) -> %s' % (self.__hash_job(job), job))

    def show_jobs(self):
        """
        Print the jobs from from crontab
        """
        print("Currently active jobs in crontab:")
        for line in self.crontab_lines[:]:
            job = self.settings.CRONTAB_LINE_REGEXP.findall(line)
            if job and job[0][4] == self.settings.CRONTAB_COMMENT:
                if self.verbosity >= 1:
                    print('%s -> %s' % (
                        job[0][2].split()[4],
                        self.__get_job_by_hash(job[0][2][job[0][2].find('run') + 4:].split()[0])
                    ))

    def remove_jobs(self):
        """
        Removes all jobs defined in CRONJOBS setting from internal buffer
        """
        for line in self.crontab_lines[:]:
            job = self.settings.CRONTAB_LINE_REGEXP.findall(line)
            if job and job[0][4] == self.settings.CRONTAB_COMMENT:
                self.crontab_lines.remove(line)
                if self.verbosity >= 1:
                    print('removing cronjob: (%s) -> %s' % (
                        job[0][2].split()[4],
                        self.__get_job_by_hash(job[0][2][job[0][2].find('run') + 4:].split()[0])
                    ))

    # noinspection PyBroadException
    def run_job(self, job_hash):
        """
        Executes the corresponding function defined in CRONJOBS
        """
        job = self.__get_job_by_hash(job_hash)
        job_name = job[1]
        job_args = job[2] if len(job) > 2 else []
        job_kwargs = job[3] if len(job) > 3 else {}

        lock_file_name = None
        if self.settings.LOCK_JOBS:
            lock_file = open(os.path.join(tempfile.gettempdir(), 'django_crontab_%s.lock' % job_hash), 'w')
            lock_file_name = lock_file.name
            try:
                fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except:
                logger.warning('Tried to start cron job %s that is already running.', job)
                return

        module_path, function_name = job_name.rsplit('.', 1)
        module = import_module(module_path)
        func = getattr(module, function_name)
        try:
            func(*job_args, **job_kwargs)
        except:
            logger.exception('Failed to complete cronjob at %s', job)

        if self.settings.LOCK_JOBS:
            try:
                os.remove(lock_file_name)
            except:
                logger.exception('Error deleting lockfile %s of job %s', lock_file_name, job)

    def __hash_job(self, job):
        """
        Builds an md5 hash representing the job
        """
        return hashlib.md5(json.dumps(job).encode('utf-8')).hexdigest()

    def __get_job_by_hash(self, job_hash):
        """
        Finds the job by given hash
        """
        for job in self.settings.CRONJOBS:
            if self.__hash_job(job) == job_hash:
                return job
        return None
