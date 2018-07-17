#!/usr/bin/env python3

from setuptools import setup

import os

def src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))

def readme():
    with open(src('README.md'), 'r') as fin:
        return ''.join(fin.readlines())

setup(
    name='sample',
    packages=['sample'],
    doc=readme(),
    version='0.0.2',
    install_requires=[
        'numpy>=1.11',
        'Jinja2',
        ],
    entry_points={
        'console_scripts': [
            'sample = sample:main',
        ],
    },
)
