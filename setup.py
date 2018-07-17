from setuptools import setup

setup(
    name='clidist',
    packages=['clidist'],
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'clidist = clidist:main',
        ],
    },
)
