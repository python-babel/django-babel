#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


with open('README.md', 'rb') as fobj:
    readme = fobj.read()


with open('CHANGES.md', 'rb') as fobj:
    history = fobj.read()


test_requires = [
    'coverage',
    'pytest',
    'pytest-cov>=1.4',
    'python-coveralls',
]


install_requires = [
    'Django>=1.4,<1.7',
    'Babel>=1.3',
]


dev_requires = [
    'flake8>=2.0',
]



class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='django-babel',
    description='Utilities for using Babel in Django',
    long_description=readme + '\n\n' + history,
    version='1.0-dev',
    license='BSD',
    author='Christopher Lenz',
    author_email='cmlenz@gmail.com',
    url='http://github.com/graingert/django-babel/',
    packages=find_packages(exclude=('tests',)),
    tests_require=test_requires,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points="""
    [babel.extractors]
    django = babeldjango.extract:extract_django
    """,
)
