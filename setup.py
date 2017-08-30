#!/usr/bin/env python2.7

from setuptools import setup
import sys, subprocess
from python_openvas.lib import __version__

(major, minor, micro) = subprocess.check_output(["openvassd","--version"]).splitlines()[0].split(' ')[2].split('.')

if (major,minor) < (5, 1):
    print "This software is not compatible with OpenVAS scanner < 5.1.0"

if sys.version_info < (2, 6):
    print "This software is not compatible with python < 2.6"
    sys.exit(-1)

setup(name='python-openvas', 	#name of pip package/project
      version = __version__ ,
      description = 'OpenVAS Scanner wrapper',
      author = 'Yohan Pipereau',
      author_email = 'yohan.pipereau@cern.ch',
      url = 'https://security.web.cern.ch/security/home/en/index.shtml',
      license = '',
      install_requires = ['progressbar'], #dependencies
      keywords=['OpenVAS'], # What does your project relate to?
      #scripts to detect
      scripts=['python_openvas/python-openvas', 'python_openvas/openvas-blacklist', 'magicredis'], 
      #package to detect:
      packages = ['python_openvas'],
      #specify lib directory as the package directory for python_openvas
      package_dir = {'python_openvas': 'python_openvas/lib'},
      #additional files:
      data_files = [('/opt/python-openvas/reports', []),
      ('/etc/python-openvas', ['python_openvas/conf/scan.conf']),
      ('/etc/python-openvas', ['python_openvas/conf/blacklist.conf']),
      ], #right path copied into left path (created if necessary)
      )
