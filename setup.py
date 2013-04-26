#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-crontab',
    description='dead simple crontab powered job scheduling for django',
    version='0.5.0',
    author='Lars Kreisz',
    author_email='der.kraiz@gmail.com',
    license='MIT',
    url='https://github.com/kraiz/django-crontab',
    long_description=open('README.rst').read(),
    packages=[
        'django_crontab',
        'django_crontab.management',
        'django_crontab.management.commands'],
    requires=[
        'Django'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup'
    ]
)
