#!/usr/bin/env python3

from setuptools import setup

import os

def src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))

def _read_file(fname, op):
    with open(src(fname), 'r') as fin:
        return op(fin.readlines())


def requirements():
    return _read_file('requirements.txt',
                      lambda lines: list(map(str.strip, lines)))

def readme():
    return _read_file('README.md',
                      lambda lines: ''.join(lines))

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
    version='0.0.4',
    install_requires=requirements(),
    entry_points={
        'console_scripts': [
            'samplitude = samplitude:main',
            's8e = samplitude:main',
        ],
    },
)
