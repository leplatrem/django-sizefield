from __future__ import unicode_literals

import re

from django.utils import formats
from django.utils import six
from django.utils.translation import ugettext as _


def filesizeformat(bytes, decimals = 1):
    """
    Formats the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 bytes, etc).
    Based on django.template.defaultfilters.filesizeformat
    """

    try:
        bytes = float(bytes)
    except (TypeError,ValueError,UnicodeDecodeError):
        raise ValueError

    filesize_number_format = lambda value: formats.number_format(round(value, decimals), decimals)

    KB =  1<<10
    MB  = 1<<20
    GB = 1<<30
    TB = 1<<40
    PB  = 1<<50

    if bytes < KB:
        return '%s B' % filesize_number_format(bytes)
    if bytes < MB:
        return '%s KB' % filesize_number_format(bytes / KB)
    if bytes < GB:
        return '%s MB' % filesize_number_format(bytes / MB)
    if bytes < TB:
        return '%s GB'% filesize_number_format(bytes / GB)
    if bytes < PB:
        return '%s TB' % filesize_number_format(bytes / TB)
    return '%s PB' % filesize_number_format(bytes / PB)


file_size_re = re.compile(r'^(?P<value>[0-9\.]+?)\s*(?P<unit>(B{0,1}|[KMGTP]{1}B{1})?)$', re.IGNORECASE)
FILESIZE_UNITS = {
    'B' : 1,
    'KB' : 1<<10,
    'MB' : 1<<20,
    'GB' : 1<<30,
    'TB' : 1<<40,
    'PB' : 1<<50,
    }

def parse_size(size):
    """
    @rtype int
    """
    if isinstance(size, six.integer_types):
        return size

    r = file_size_re.match(size)
    if r:
        value = float(r.group('value'))
        unit  = r.group('unit').upper() or 'B'
        return int(value * FILESIZE_UNITS[unit])

    # Regex pattern was not matched
    raise ValueError(_("Size '%s' has incorrect format") % size)