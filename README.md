# about
dead simple crontab powered job scheduling for django.

# setup
install via easy_install or pip

        easy_install django-crontab

add installed apps in django settings.py

        INSTALLED_APPS = (
            'django_crontab',
            ...
        )

now create a new method that should be scheduled by cron, f.e. in `myproject/myapp/cron.py`

        def my_scheduled_job():
          pass

now add this your settings.py:

        CRONJOBS = [
            ('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')
        ]

the least to do is to run the command to add all defined jobs from `CRONJOBS` to crontab:

        python manage.py crontab add

removing all defined jobs is straight forward

        python manage.py crontab remove

# config
there are a bunch of setting vars to customize behavior. each of this comes with default values that should properly fit.

* CRONJOBS
  * list of tuples with cron timing and the python module path to the method
  * default: []
  * example
        
            CRONJOBS = [
                ('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job'),
                ('0   0 1 * *', 'myproject.myapp.cron.other_scheduled_job'),
                ('@reboot',     'myproject.anotherapp.cron.system_reboot_job'),
            ]

* CRONTAB\_EXECUTABLE
  * path to the crontab executable of your os
  * default: '/usr/bin/crontab'

* CRONTAB\_DJANGO\_PROJECT\_NAME
  * the name of your django project, used to build path path to manage.py
  * default is read from DJANGO_SETTINGS_MODULE environment variable 

* CRONTAB\_DJANGO\_MANAGE\_PATH
  * path to manage.py file
  * default is build using DJANGO\_PROJECT\_NAME

* CRONTAB\_PYTHON\_EXECUTABLE
  * path to the python interpreter executable used to run the scheduled job
  * default uses the interpreter executable used to `add` the jobs

* CRONTAB\_COMMAND\_PREFIX
  * something you wanne do before job gets executed.
  * default: '' (empty string) 
  * example: '`echo "executing my scheduled job now" && `'

* CRONTAB\_COMMAND\_SUFFIX
  * something you wanne do after job was executed.
  * default: '' (empty string) 
  * example: '` && echo "execution of my scheduled job finished"`'

# license
MIT-License, see [LICENSE](/kraiz/django-cronjobs/blob/master/LICENSE/) file.