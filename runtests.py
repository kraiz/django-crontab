#!/usr/bin/env python
import os
import sys

import django
from django.test.runner import DiscoverRunner


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    django.setup()

    labels = sys.argv[1:] or ['tests']
    runner = DiscoverRunner(verbosity=1, interactive=False)
    failures = runner.run_tests(labels)
    sys.exit(bool(failures))


if __name__ == '__main__':
    main()
