#!/usr/bin/env python2.7

import os
from setuptools import setup

setup(name='python-openvas',
      version = os.getenv('VERSION'),
      description = 'OpenVAS Scanner wrapper',
      long_description = 'Python wrapper for OpenVAS Scanner',
      author = 'Yohan Pipereau',
      author_email = 'yohan.pipereau@gmail.com',
      url = 'https://github.com/YohanPipereau/python-openvas',
      license = 'GPL3',
      platforms = 'Linux',
      install_requires = ['progressbar', 'requests'], # Dependencies
      keywords=['OpenVAS'], # What does your project relate to?
      #scripts to detect
      scripts=['python_openvas/python-openvas', 'python_openvas/openvas-blacklist', 'magicredis'],
      #package to detect:
      packages = ['python_openvas'],
      # Specify lib directory as the package directory for python_openvas
      package_dir = {'python_openvas': 'python_openvas/lib'},
      # Additional files:
      data_files = [('/opt/python-openvas/reports', []),
      ('/opt/python-openvas/etc', ['python_openvas/conf/scan.conf']),
      ('/opt/python-openvas/etc', ['python_openvas/conf/blacklist.conf']),
      ], #right path copied into left path (created if necessary)
      )
