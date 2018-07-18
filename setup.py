#!/usr/bin/env python3

from setuptools import setup

import os

def src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))

def readme():
    with open(src('README.md'), 'r') as fin:
        return ''.join(fin.readlines())

__pgdr = 'PG Drange <pgdr@equinor.com>'
__source = 'https://github.com/pgdr/samplitude'
__webpage = __source

setup(
    name='samplitude',
    packages=['samplitude'],
    description=readme(),
    author='PG Drange',
    author_email='pgdr@equinor.com',
    maintainer=__pgdr,
    url=__webpage,
    project_urls={
        'Bug Tracker': '{}/issues'.format(__source),
        'Documentation': '{}/blob/master/README.md'.format(__source),
        'Source Code': __source,
    },
    license='GNU GPL v3 or later',
    keywords='jinja2 jinja random statistics sample distribution plot',
    version='0.0.2',
    install_requires=[
        'numpy>=1.11',
        'Jinja2',
        ],
    entry_points={
        'console_scripts': [
            'samplitude = samplitude:main',
        ],
    },
)
