# about
dead simple crontab powered job scheduling for django.

# setup
install via easy_install or pip

        easy_install django-crontab

add it to installed apps in django settings.py

        INSTALLED_APPS = (
            'django_crontab',
            ...
        )

now create a new method that should be executed by cron every 5 minutes, f.e. in `myproject/myapp/cron.py`

        def my_scheduled_job():
          pass

now add this to your settings.py:

        CRONJOBS = [
            ('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job')
        ]

the least to do is to run this command to add all defined jobs from `CRONJOBS` to crontab (of the user which you are running this command with):

        python manage.py crontab add

removing all defined jobs is straight forward

        python manage.py crontab remove

# config
there are a bunch of setting vars to customize behavior. each of this comes with default values that should properly fit. if not, feel free to overwrite.

* CRONJOBS
  * list of tuples with cron timing, the python module path to the method and optional a job specific suffix (f.e. to redirect out/err to a file)
  * default: []
  * example
        
            CRONJOBS = [
                ('*/5 * * * *', 'myproject.myapp.cron.my_scheduled_job'),
                ('0   0 1 * *', 'myproject.myapp.cron.other_scheduled_job'),
                ('@reboot',     'myproject.anotherapp.cron.system_reboot_job', '>> /home/john/web/logs/system_reboot_job.log'),
            ]

* CRONTAB\_EXECUTABLE
  * path to the crontab executable of your os
  * default: '/usr/bin/crontab'

* CRONTAB\_DJANGO\_PROJECT\_NAME
  * the name of your django project, used to build path path to manage.py and to mark the jobs in contrab via comment for later removing
  * default is read from DJANGO_SETTINGS_MODULE environment variable 

* CRONTAB\_DJANGO\_MANAGE\_PATH
  * path to manage.py file (including the manage.py itself, i.e. '/home/john/web/manage.py')
  * default is build using DJANGO\_PROJECT\_NAME

* CRONTAB\_PYTHON\_EXECUTABLE
  * path to the python interpreter executable used to run the scheduled job
  * default uses the interpreter executable used to `add` the jobs (via 'python manage.py crontab add')

* CRONTAB\_COMMAND\_PREFIX
  * something you wanne do before job gets executed.
  * default: '' (empty string) 
  * example: '`echo "executing my scheduled job now" && `'

* CRONTAB\_COMMAND\_SUFFIX
  * something you wanne do after job was executed.
  * default: '' (empty string) 
  * example: '` && echo "execution of my scheduled job finished"`'

* CRONTAB\_COMMENT
  * used for marking the added contab-lines for removing, default value includes project name to distinguish multiple projects on the same host and user
  * default: 'django-crontabs for ' + CRONTAB\_DJANGO\_PROJECT\_NAME

# license
MIT-License, see [LICENSE](/kraiz/django-crontab/blob/master/LICENSE) file.
