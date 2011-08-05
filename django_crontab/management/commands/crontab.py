from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from django_crontab.app_settings import CRONTAB_EXECUTABLE, CRONJOBS, \
    CRONTAB_LINE_PATTERN, CRONTAB_COMMENT, PYTHON_EXECUTABLE, DJANGO_MANAGE_PATH, \
    CRONTAB_LINE_REGEXP, COMMAND_PREFIX, COMMAND_SUFFIX
import os
import tempfile

class Command(BaseCommand):
    args = '<add|remove>'
    help = 'run this command to add or remove the jobs defined in CRONJOBS setting from/to crontab'
    crontab_lines = []


    def handle(self, *args, **options):
        """dispatches by given subcommand"""
        if len(args) > 0:
            if args[0] == 'add':
                self.__read_crontab(**options)
                self.__remove_cronjobs(*args, **options)
                self.__add_cronjobs(*args, **options)
                self.__write_crontab(**options)
                return
            elif args[0] == 'remove':
                self.__read_crontab(**options)
                self.__remove_cronjobs(*args, **options)
                self.__write_crontab(**options)
                return
            elif args[0] == 'run':
                self.__run_cronjob(args[1])
                return
        print help


    def __read_crontab(self, **options):
        """reads the crontab into internal buffer"""
        if options.get('verbosity') == '2':
            print 'reading from crontab...',
        self.crontab_lines = os.popen('%s -l' % CRONTAB_EXECUTABLE).readlines()
        if options.get('verbosity') == '2':
            print 'done'


    def __write_crontab(self, **options):
        """writes internal buffer back to crontab"""
        if options.get('verbosity') == '2':
            print 'writing to crontab...',
        fd, path = tempfile.mkstemp()
        tmp = os.fdopen(fd, 'w')
        for line in self.crontab_lines:
            tmp.write(line)
        tmp.close()
        os.system('%s %s' % (CRONTAB_EXECUTABLE, path))
        os.unlink(path)
        if options.get('verbosity') == '2':
            print 'done'


    def __add_cronjobs(self, *args, **options):
        """adds all jobs defined in CRONJOBS setting to internal buffer"""
        for cronjob in CRONJOBS:
            self.crontab_lines.append(CRONTAB_LINE_PATTERN % {
                'time': cronjob[0],
                'comment': CRONTAB_COMMENT,
                'command': '%(global_prefix)s %(exec)s %(manage)s crontab run %(jobname)s %(job_suffix)s %(global_suffix)s' % {
                    'global_prefix': COMMAND_PREFIX,
                    'exec': PYTHON_EXECUTABLE,
                    'manage': DJANGO_MANAGE_PATH,
                    'jobname': cronjob[1],
                    'job_suffix': cronjob[2] if len(cronjob) > 2 else '',
                    'global_suffix': COMMAND_SUFFIX
                }
            })
            if options.get('verbosity') == '1':
                print '  adding cronjob: %s -> %s' % cronjob[:2]
            elif options.get('verbosity') == '2':
                print 'adding cronjob: %s' % self.crontab_lines[-1],


    def __remove_cronjobs(self, *args, **options):
        """removes all jobs defined in CRONJOBS setting from internal buffer"""
        for line in self.crontab_lines:
            job = CRONTAB_LINE_REGEXP.findall(line)
            if job and job[0][4] == CRONTAB_COMMENT:
                self.crontab_lines.remove(line)
                if options.get('verbosity') == '1':
                    print 'removing cronjob: %s -> %s' % (job[0][0].strip(), job[0][2][job[0][2].find('run') + 4:].split()[0])
                elif options.get('verbosity') == '2':
                    print 'removing cronjob: %s ' % line,


    def __run_cronjob(self, function):
        """executes the corresponding function defined in CRONJOBS"""
        for cronjob in CRONJOBS:
            if cronjob[1] == function:
                module_path, function_name = function.rsplit('.', 1)
                module = import_module(module_path)
                func = getattr(module, function_name)
                func()

