# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='python-nygma',
    version='0.0.1',
    description=(
        'Enigma cipher machine implemented in Python '
        'with option to encrypt arbitrary data.'
    ),
    long_description=long_description,
    url='https://github.com/escer/python-nygma',
    author='Pawel Scierski',
    author_email='escer@protonmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security :: Cryptography',
    ],
    keywords='python enigma cryptography',
    packages=find_packages(),
)
