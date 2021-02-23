#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'requests==2.24.0' ]

# setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', 'responses>=0.10.16']

setup(
    author="Volker Kempert",
    author_email='volker.kempert@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Log data from 3 phase ac measurement unit",
    entry_points={
        'console_scripts': [
            'pcl=power_consumption_logger.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='power_logger',
    name='power_logger',
    packages=find_packages(include=['power_consumption_logger', 'power_consumption_logger.*']),
    # setup_requires=setup_requirements,
    test_suite='tests',
    # tests_require=test_requirements,
    url='https://github.com/volker-kempert/power_logger',
    version='0.1.0',
    zip_safe=False,
)
