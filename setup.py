from setuptools import setup

setup(
    name='clidist',
    packages=['clidist'],
    version='0.0.1',
    install_requires=[
        'numpy>=1.11',
        'Jinja2',
        ],
    entry_points={
        'console_scripts': [
            'clidist = clidist:main',
        ],
    },
)
