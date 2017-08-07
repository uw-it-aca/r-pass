#!/usr/bin/env python

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/r-pass>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'r_pass/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='RPass',
    version=VERSION,
    packages=['r_pass'],
    include_package_data=True,
    install_requires = [
        'Django==1.10.5',
        'django-fields',
        'django-compressor',
        'django-fernet-fields',
        'markdown2',
        'AuthZ-Group>=1.6',
        'UW-RestClients-GWS>=0.3,<1.0',
        'UW-RestClients-Django-Utils>=0.6.5,<1.0',
    ],
    license='Apache License, Version 2.0',
    description='UW password manager',
    long_description=README,
    url='https://github.com/uw-it-aca/r-pass',
    author = "UW-IT AXDD",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
