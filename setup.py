#!/usr/bin/env python

import os
from distutils.core import setup

this_dir = os.path.dirname(__file__)
version = '0.1'

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name='python-opencongress',
    version=version,
    url='http://github.com/cpharmston/python-opencongress',
    author='Chuck Harmston',
    author_email='cpharmston@gmail.com',
    license='Dual-licensed under MIT and GPL',
    packages=['opencongress'],
    package_dir={'opencongress': 'opencongress'},
    description='A Python interface to the OpenCongress.org API',
    classifiers=classifiers,
    long_description=open(os.path.join(this_dir, 'README.rst')).read(),
)