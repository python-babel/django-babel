#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


test_requires = [
    'coverage',
    'pytest',
    'pytest-cov>=1.4',
    'pytest-flakes',
    'pytest-pep8',
    'python-coveralls',
]


install_requires = [
    'django>=1.4,<1.9',
    'babel>=1.3',
]


dev_requires = [
    'flake8>=2.0',
    'invoke',
    'twine'
]

setup(
    name='django-babel',
    description='Utilities for using Babel in Django',
    long_description=read('README.rst') + u'\n\n' + read('CHANGELOG.rst'),
    version='0.4.0',
    license='BSD',
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='http://github.com/graingert/django-babel/',
    packages=find_packages(exclude=('tests',)),
    tests_require=test_requires,
    install_requires=install_requires,
    extras_require={
        'docs': ['sphinx'],
        'tox': ['tox'],
        'tests': test_requires,
        'dev': dev_requires,
    },
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'babel.extractors': [
            'django = django_babel.extract:extract_django',
        ]
    }
)
