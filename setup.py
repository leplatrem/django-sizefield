#!/usr/bin/python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages

setup(name         = 'django-sizefield',
      version      = '0.1',
      license      = 'LGPL',
      description  = 'A model field to store a file size, whose edition and display shows units.',
      author       = "Mathieu Leplatre",
      author_email = "contact@mathieu-leplatre.info",
      url          = "http://code.mathieu-leplatre.info/projects/show/django-sizefield",
      download_url = "http://code.mathieu-leplatre.info/repositories/show/django-sizefield",
      long_description = """\
django-sizefield
----------------

A file size field, stored as BigInteger and rendered with units in Bytes (KB, MB, ...)


Examples
--------
With a model like ::


    class Data(models.Model):
        path = models.FilePathField()
        size = FileSizeField()

In templates ::

    {% load sizefieldtags %}
    
    {{ data.size|filesize }}
    
*will render 12.3KB (for example)*

The model form will have a TextInput, which renders the 
value with units, and accepts values with or without units.
""",
      provides     = ['sizefield'],
      packages     = find_packages(),
      platforms    = ('any',),
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
