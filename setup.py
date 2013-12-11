#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Edgewall Software
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://babel.edgewall.org/wiki/License.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://babel.edgewall.org/log/.

from setuptools import setup, find_packages

setup(
    name = 'django-babel',
    description = 'Utilities for using Babel in Django',
    version='0.3.1',
    license = 'BSD',
    author  = 'Edgewall Software',
    author_email = 'python-babel@googlegroups.com',
    url = 'http://github.com/graingert/django-babel/',
    packages = find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    install_requires = ['Babel'],

    entry_points = """
    [babel.extractors]
    django = babeldjango.extract:extract_django
    """,
)
