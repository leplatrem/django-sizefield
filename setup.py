#!/usr/bin/python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages

f = open('README')
readme = f.read()
f.close()

setup(name         = 'django-sizefield',
      version      = '0.3',
      license      = 'LGPL',
      description  = 'A model field to store a file size, whose edition and display shows units.',
      author       = "Mathieu Leplatre",
      author_email = "contact@mathieu-leplatre.info",
      url          = "http://code.mathieu-leplatre.info/projects/show/django-sizefield",
      download_url = "http://code.mathieu-leplatre.info/repositories/show/django-sizefield",
      long_description = readme,
      provides     = ['sizefield'],
      packages     = find_packages(),
      keywords     = ['django', 'field', 'filesize'],
      classifiers  = ['Programming Language :: Python :: 2.5',
                      'Operating System :: OS Independent',
                      'Environment :: Web Environment',
                      'Intended Audience :: Developers',
                      'Framework :: Django',
                      'Natural Language :: English',
                      'Topic :: Utilities',
                      'Development Status :: 5 - Production/Stable'],
) 
