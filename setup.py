"""A setuptools based setup module for YNG-Manipulate"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'click',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='YNG-Manipulate',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="3D Zone Printing",
    long_description=readme + '\n\n' + history,
    author="YNG LLC",
    author_email='yngwebtech@gmail.com',
    url='https://github.com/yngsoftwaredev/manipulate',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts':[
            'manipulate=yng_manipulate.cli:cli',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="GNU AGPLv3",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved ::  GNU AFFERO GENERAL PUBLIC LICENSE',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
