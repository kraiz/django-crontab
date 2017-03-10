from __future__ import print_function

from django.core.management.base import BaseCommand
from django_crontab.crontab import Crontab


class Command(BaseCommand):
    """
    Define the Django management commands add, show, remove and run
    run takes an additional `jobhash` argument specifying which job to run
    """

    help = 'run this command to add, show or remove the jobs defined in CRONJOBS setting from/to crontab'

    def add_arguments(self, parser):
        parser.add_argument('subcommand', choices=['add', 'show', 'remove', 'run'])
        parser.add_argument('jobhash', nargs='?')

    def handle(self, *args, **options):
        """
        Dispatches by given subcommand
        """
        if options['subcommand'] == 'add':         # add command
            with Crontab(**options) as crontab:    # initialize a Crontab class with any specified options
                crontab.remove_jobs()              # remove all jobs specified in settings from the crontab
                crontab.add_jobs()                 # and add them back
        elif options['subcommand'] == 'show':      # show command
            # initialize a readonly Crontab class with any specified options
            with Crontab(readonly=True, **options) as crontab:
                crontab.show_jobs()                # list all currently active jobs from crontab
        elif options['subcommand'] == 'remove':    # remove command
            with Crontab(**options) as crontab:    # initialize a Crontab class with any specified options
                crontab.remove_jobs()              # remove all jobs specified in settings from the crontab
        elif options['subcommand'] == 'run':       # run command
            Crontab().run_job(options['jobhash'])  # run the job with the specified hash
        else:
            # output the help string if the user entered something not specified above
            print(self.help)
