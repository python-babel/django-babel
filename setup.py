#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'BabelDjango',
    description = 'Utilities for using Babel in Django',
    version = '1.0-dev',
    license = 'BSD',
    author  = 'Christopher Lenz',
    author_email = 'cmlenz@gmail.com',
    url = 'https://github.com/cmlenz/django-babel',

    packages = ['babeldjango', 'babeldjango.templatetags'],
    install_requires = ['Babel'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    entry_points = """
    [babel.extractors]
    django = babeldjango.extract:extract_django
    """,
)
