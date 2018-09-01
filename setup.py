#!/usr/bin/env python

from runpy import run_path
from pathlib import Path
from setuptools import setup, find_packages


VERSION = run_path(
    str(Path(__file__).parent) + '/pipeline_live/_version.py')['__version__']

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='pipeline-live',
    version=VERSION,
    description='Zipline Pipeline extension for live trade',
    long_description=README,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    author='Alpaca',
    author_email='oss@alpaca.markets',
    url='https://github.com/alpacahq/pipeline-live',
    keywords='financial,zipline,pipeline,stock,screening,api,trade',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial',
    ],
    packages=find_packages(),
    install_requires=[
        'alpaca-trade-api',
        'iexfinance',
        'zipline==1.3.0',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'flake8',
    ],
    setup_requires=['pytest-runner', 'flake8'],
)
