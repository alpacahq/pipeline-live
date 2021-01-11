#!/usr/bin/env python

import ast
import re
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pipeline_live/_version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='pipeline-live',
    version=version,
    description='Zipline Pipeline extension for live trade',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Alpaca',
    author_email='oss@alpaca.markets',
    url='https://github.com/alpacahq/pipeline_live',
    keywords='financial,zipline,pipeline,stock,screening,api,trade',
    packages=find_packages(),
    install_requires=[
        'pandas==0.22.0',
        'numpy==1.18.4',
        'alpaca-trade-api>=0.51.0',
        'iexfinance>=0.4.1,<0.5.0',
        'zipline==1.3.0',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'flake8',
    ],
    setup_requires=['pytest-runner', 'flake8'],
)
