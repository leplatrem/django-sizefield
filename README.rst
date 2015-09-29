*django-sizefield* is a file size field, stored as BigInteger and rendered
with units in Bytes (KB, MB, KiB, Mib, ...)

.. image:: https://travis-ci.org/leplatrem/django-sizefield.png
    :target: https://travis-ci.org/leplatrem/django-sizefield

.. image:: https://coveralls.io/repos/leplatrem/django-sizefield/badge.png
    :target: https://coveralls.io/r/leplatrem/django-sizefield


=======
INSTALL
=======

::

    pip install django-sizefield


=====
USAGE
=====

Model field
===========

::

    class Data(models.Model):
        path = models.FilePathField()
        size = FileSizeField()


The model form will have a TextInput, which renders the 
value with units, and accepts values with or without units.

::

    size = FileSizeField(is_binary=False)

It is possible to have fields with decimal size. In this
instance, a value of 1KB would be parsed as 1000 bytes.


Template filter
===============

It adds units to any number value:

::

    {% load sizefieldtags %}
    
    {{ value|filesize }}

*will render 12.3KB (for example)*

To explicitly declare the type of formatting desired, use:

::

    {% custom_filesize 1024 binary=True ambiguous_suffix=False %}

*will render as 1KiB*


Settings
========

By default, 1KB and 1KiB will both parse to 1024 bytes.

::

    SIZEFIELD_IS_BINARY = False
    SIZEFIELD_AMBIGUOUS_SUFFIX = False
    SIZEFIELD_ASSUME_BINARY = False

With settings similar to the above, the default will assume
that 1KB represents 1000 bytes. Formatting from byte values
will also follow this rule.


=======
AUTHORS
=======

    * Mathieu Leplatre <contact@mathieu-leplatre.info>
    * Alexander (@meteozond)
    * Tom Yam (@perez)
    * William Tucker <william.tucker@stfc.ac.uk>


=======
LICENSE
=======

    * Lesser GNU Public License





