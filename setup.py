#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-crontab',
    description='dead simple crontab powered job scheduling for django',
    version='0.6.0',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Installation/Setup'
    ]
)
