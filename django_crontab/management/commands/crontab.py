from __future__ import print_function

from django.core.management.base import BaseCommand
from django_crontab.crontab import Crontab


class Command(BaseCommand):
    args = '<add|show|remove>'
    help = 'run this command to add, show or remove the jobs defined in CRONJOBS setting from/to crontab'
    crontab_lines = []

    def handle(self, *args, **options):
        """
        Dispatches by given subcommand
        """
        if len(args) > 0:
            if args[0] == 'add':
                with Crontab(**options) as crontab:
                    crontab.remove_jobs()
                    crontab.add_jobs()
                return
            elif args[0] == 'show':
                with Crontab(readonly=True, **options) as crontab:
                    crontab.show_jobs()
                return
            elif args[0] == 'remove':
                with Crontab(**options) as crontab:
                    crontab.remove_jobs()
                return
            elif args[0] == 'run':
                Crontab().run_job(args[1])
                return
        print(help)
