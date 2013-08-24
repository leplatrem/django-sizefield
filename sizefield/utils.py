from __future__ import unicode_literals

import re
import operator

from django.utils import formats
from django.utils import six
from django.utils.translation import ugettext as _
from django.conf import settings


SIZEFIELD_FORMAT = getattr(settings, 'SIZEFIELD_FORMAT', '{value}{unit}')

file_size_re = re.compile(r'^(?P<value>[0-9\.]+?)\s*(?P<unit>(B{0,1}|[KMGTP]{1}B{1})?)$', re.IGNORECASE)
FILESIZE_UNITS = {
    'B' : 1,
    'KB' : 1<<10,
    'MB' : 1<<20,
    'GB' : 1<<30,
    'TB' : 1<<40,
    'PB' : 1<<50,
    }


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

    units_list = sorted(six.iteritems(FILESIZE_UNITS), key=operator.itemgetter(1))

    value = unit = None
    len_unints_list = len(units_list)
    for i in xrange(1, len_unints_list):
        if bytes < units_list[i][1]:
            prev_unit = units_list[i-1]
            value = filesize_number_format(bytes / prev_unit[1])
            unit = prev_unit[0]
            break

    if value is None:
        value = filesize_number_format(bytes / units_list[len_unints_list][1])
        unit = units_list[len_unints_list][0]

    return SIZEFIELD_FORMAT.format(value = value, unit = unit)

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