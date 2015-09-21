#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requires = [
    'Django>=1.4,<1.9',
    'Babel>=1.3',
]


setup(
    name='django-babel',
    description='Utilities for using Babel in Django',
    long_description=read('README.rst') + u'\n\n' + read('CHANGELOG.rst'),
    version='0.4-dev',
    license='BSD',
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    maintainer='Thomas Grainger',
    maintainer_email='django-babel@graingert.co.uk',
    url='https://github.com/graingert/django-babel/',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'Django>=1.4,<1.8',
        'Babel>=1.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'babel.extractors': [
            'django = babeldjango.extract:extract_django',
        ]
    }
)
