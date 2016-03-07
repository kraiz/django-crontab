#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-crontab',
    description='dead simple crontab powered job scheduling for django',
    version='0.7.1',
    author='Lars Kreisz',
    author_email='lars.kreisz@gmail.com',
    license='MIT',
    url='https://github.com/kraiz/django-crontab',
    long_description=open('README.rst').read(),
    packages=[
        'django_crontab',
        'django_crontab.management',
        'django_crontab.management.commands'],
    install_requires=[
        'Django>=1.8'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Installation/Setup'
    ]
)
