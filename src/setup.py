#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'uWSGI==2.0.18',
    'boto3==1.9.172',
    'Click==7.0',
    'Flask==1.0.3',
    'flask-restplus==0.12.1',
    'flask-cors',
    'pynamodb==3.4.0',
    'marshmallow==2.19.5',
                ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="MT AWS Dev",
    author_email='cloudservices@mediatemple.net',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    description="MT AWS Tools & API",
    entry_points={
        'console_scripts': [
            'mtaws=mtaws.cli:main',
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords='mtaws',
    name='mtaws',
    packages=find_packages(include=['mtaws']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mediatemple/mtaws',
    version='0.1.1',
    zip_safe=False,
)
