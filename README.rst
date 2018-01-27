.. image:: https://img.shields.io/travis/kraiz/django-crontab/master.svg
    :target: https://travis-ci.org/kraiz/django-crontab
.. image:: https://img.shields.io/coveralls/kraiz/django-crontab/master.svg
    :target: https://coveralls.io/r/kraiz/django-crontab
.. image:: https://img.shields.io/pypi/dw/django-crontab.svg
    :target: https://pypi.python.org/pypi/django-crontab
.. image:: https://img.shields.io/pypi/v/django-crontab.svg
    :target: https://pypi.python.org/pypi/django-crontab
.. image:: https://img.shields.io/pypi/pyversions/django-crontab.svg
    :target: https://pypi.python.org/pypi/django-crontab
.. image:: https://img.shields.io/pypi/l/django-crontab.svg
    :target: https://pypi.python.org/pypi/django-crontab

about
=====

dead simple crontab powered job scheduling for django (1.8+).

setup
=====
install via pip:

.. code:: bash

    pip install django-crontab

add it to installed apps in django settings.py:

.. code:: python

    INSTALLED_APPS = (
        'django_crontab',
        ...
    )

now create a new method that should be executed by cron every 5 minutes, f.e. in `myapp/cron.py`:

.. code:: python

    def my_scheduled_job():
      pass

now add this to your settings.py:

.. code:: python

    CRONJOBS = [
        ('*/5 * * * *', 'myapp.cron.my_scheduled_job')
    ]

you can also define positional and keyword arguments which let you call django management commands:

.. code:: python

    CRONJOBS = [
        ('*/5 * * * *', 'myapp.cron.other_scheduled_job', ['arg1', 'arg2'], {'verbose': 0}),
        ('0   4 * * *', 'django.core.management.call_command', ['clearsessions']),
    ]

finally run this command to add all defined jobs from `CRONJOBS` to crontab (of the user which you are running this command with):

.. code:: bash

    python manage.py crontab add

show current active jobs of this project:

.. code:: bash

    python manage.py crontab show

removing all defined jobs is straight forward:

.. code:: bash

    python manage.py crontab remove

config
======
there are a bunch of setting vars to customize behavior. each of them comes with default values that should properly fit. if not, feel free to overwrite.

CRONJOBS
  - list of jobs, each defined as tuple:

    - format 1:

      1. required: cron timing in usual format (see `Wikipedia <http://en.wikipedia.org/wiki/Cron#Format>`_ and `crontab.guru <https://crontab.guru/examples.html>`_ for more examples)
      2. required: the python module path to the method
      3. optional: a job specific suffix (f.e. to redirect out/err to a file, default: '')

    - format 2:

      1. required: cron timing
      2. required: the python module path to the method
      3. optional: list of positional arguments for the method (default: [])
      4. optional: dict of keyword arguments for the method (default: {})
      5. optional: a job specific suffix (f.e. to redirect out/err to a file, default: '')

  - NOTE: Run "python manage.py crontab add" each time you change CRONJOBS in any way!
  - default: []
  - example:

    .. code:: python

        CRONJOBS = [
            ('*/5 * * * *', 'myapp.cron.my_scheduled_job'),

            # format 1
            ('0   0 1 * *', 'myapp.cron.my_scheduled_job', '>> /tmp/scheduled_job.log'),

            # format 2
            ('0   0 1 * *', 'myapp.cron.other_scheduled_job', ['myapp']),
            ('0   0 * * 0', 'django.core.management.call_command', ['dumpdata', 'auth'], {'indent': 4}, '> /home/john/backups/last_sunday_auth_backup.json'),
        ]

CRONTAB_LOCK_JOBS
  - prevent starting a job if an old instance of the same job is still running
  - default: False
  - since 0.5.0

CRONTAB_EXECUTABLE
  - path to the crontab executable of your os
  - default: '/usr/bin/crontab'

CRONTAB_DJANGO_PROJECT_NAME
  - the name of your django project, used to build path path to manage.py and to mark the jobs in contrab via comment for later removing
  - default is read from DJANGO_SETTINGS_MODULE environment variable

CRONTAB_DJANGO_MANAGE_PATH
  - path to manage.py file (including the manage.py itself, i.e. '/home/john/web/manage.py')
  - default is build using DJANGO_PROJECT_NAME

CRONTAB_DJANGO_SETTINGS_MODULE
  - dotted python path to the settings module to run the command with
  - default is the common one from the environment variable and will not be overwritten
  - since 0.6.0

CRONTAB_PYTHON_EXECUTABLE
  - path to the python interpreter executable used to run the scheduled job
  - default uses the interpreter executable used to `add` the jobs (via 'python manage.py crontab add')

CRONTAB_COMMAND_PREFIX
  - something you want to do or declare, before each job gets executed. A good place for environment variables.
  - default: '' (empty string)
  - example: 'STAGE=production'

CRONTAB_COMMAND_SUFFIX
  - something you want to do after each job was executed.
  - default: '' (empty string)
  - example: '2>&1'

CRONTAB_COMMENT
  - used for marking the added contab-lines for removing, default value includes project name to distinguish multiple projects on the same host and user
  - default: 'django-crontabs for ' + CRONTAB_DJANGO_PROJECT_NAME

contributors
============
arski cinghiale meric426 justdoit0823 chamaken

faq
===
* **I'm using this old django version (<1.8) and can't install this package. What should i do?**
  - Yeah, update django of course (!) or - as you seem to be familiar with old, unsupported versions, install the old version of this package too (it support django 1.3-1.7)::

    pip install django-crontab==0.6.0

* **Will it work with windows?**
  - No.
* **Will it work within a docker?**
  - Not immediately, you need to start the cron service.
* **Problems with `pyenv`?**
  - You maybe need to setup the PATH variable within crontab. Have a look at `#60 </../../issues/60>`_
* **I'm getting "bad command"/"errors in cronfile" while installing via "crontab add". What's wrong?**
  - Maybe it's your cron time format, it can have 5 or 6 fields. Check that your system supports 6 or just define 5 in `CRONJOBS`. (see #23)
* **Why does the LOGGING not work when started via cronjob?**
  - That's maybe somehting about the current working dir. Please set your FileHandler's file path absolute and try again. (see `#31 </../../issues/31>`_)

license
=======
MIT-License, see LICENSE file.
