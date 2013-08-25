*django-sizefield* is a file size field, stored as BigInteger and rendered
with units in Bytes (KB, MB, ...)

.. image:: https://travis-ci.org/makinacorpus/django-sizefield.png
    :target: https://travis-ci.org/makinacorpus/django-sizefield

.. image:: https://coveralls.io/repos/makinacorpus/django-sizefield/badge.png
    :target: https://coveralls.io/r/makinacorpus/django-sizefield


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


Template filter
===============

It adds units to any number value:

::

    {% load sizefieldtags %}
    
    {{ value|filesize }}

*will render 12.3KB (for example)*


=======
AUTHORS
=======

    * Mathieu Leplatre <mathieu.leplatre@makina-corpus.com>
    * Alexander (@meteozond)
    * Tom Yam (@perez)


=======
LICENSE
=======

    * Lesser GNU Public License





