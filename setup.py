#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

file_dir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    filepath = os.path.join(file_dir, filename)
    return open(filepath).read()

setup(
    name="django-subdomain-instances",
    version='0.10.3',
    description='A way of allowing subdomains to be served by the same project, '
                'and associating objects with particular subdomains.',
    long_description=read_file('README.rst'),
    author='mySociety',
    author_email='matthew@mysociety.org',
    url='https://github.com/mysociety/django-subdomain-instances',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django >= 1.4, < 1.8',
    ],
    classifiers=[
        'Framework :: Django',
    ],
)
