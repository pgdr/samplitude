#!/usr/bin/env python

from setuptools import setup

setup(
    name='sample',
    packages=['sample'],
    version='0.0.1',
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
