#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages

version = '0.1'

setup(
    name='django-simple-search2',
    version=version,
    description='Django simple search module.',
    author='Filip Rec',
    author_email='filiprec@outlook.com',
    url='https://github.com/zefj/django-simple-search2',
    zip_safe=False,
    packages=['django_simple_search2'],
    
    install_requires=[
        'Django',
    ],
    include_package_data=True,
)
