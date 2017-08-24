#!/usr/bin/env python2.7

from setuptools import setup
import sys, subprocess
from python-openvas import __version__

(major, minor, micro) = subprocess.check_output(["openvassd","--version"]).splitlines()[0].split(' ')[2].split('.')

if (major,minor) < (5, 1):
    print "This software is not compatible with OpenVAS scanner < 5.1.0"

if sys.version_info < (2, 6):
    print "This software is not compatible with python < 5.1.0"
    sys.exit(-1)

setup(name='python-openvas',
      version = __version__ ,
      description = 'OpenVAS Scanner wrapper',
      author = 'Yohan Pipereau',
      author_email = 'yohan.pipereau@cern.ch',
      url = 'https://security.web.cern.ch/security/home/en/index.shtml',
      license = '',
      packages = ['python-openvas'],
      py_modules = ['python-openvas'],
      install_requires = ['progressbar'],
      data_files = [('config', ['conf/blacklist.conf', 'conf/scan.conf']),
      ('reports', ['/opt/openvas/reports'])
      ],
      )
