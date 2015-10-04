#!/usr/bin/python
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-sizefield',
    version='0.8',
    author='Mathieu Leplatre',
    author_email='contact@mathieu-leplatre.info',
    url='https://github.com/leplatrem/django-sizefield',
    download_url="http://pypi.python.org/pypi/django-sizefield/",
    description="A model field to store a file size, whose edition and display shows units.",
    long_description=open(os.path.join(here, 'README.rst')).read() + '\n\n' +
                     open(os.path.join(here, 'CHANGES')).read(),
    license='LPGL, see LICENSE file.',
    install_requires=[
        'Django',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Topic :: Utilities', 
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Development Status :: 5 - Production/Stable',
                 'Programming Language :: Python :: 2.7'],
)
