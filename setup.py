#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    import multiprocessing
except ImportError:
    pass

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from email.utils import parseaddr
import safe

author, author_email = parseaddr(safe.__author__)


def fread(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='Safe',
    version=safe.__version__,
    author=author,
    author_email=author_email,
    url='https://github.com/lepture/safe',
    packages=["safe"],
    description="Is your password safe?",
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    long_description=fread('README.rst'),
    license='BSD',
    install_requires=[],
    tests_require=['nose'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)