from __future__ import unicode_literals

import re
import operator

from django.utils import formats
from django.utils import six
from django.utils.translation import ugettext as _
from django.conf import settings


SIZEFIELD_FORMAT = getattr(settings, 'SIZEFIELD_FORMAT', '{value}{unit}')

DEFAULT_BYTE_SUFFIX = 'B'
BINARY_BYTE_SUFFIX = 'iB'
UNIT_FORMAT = '{unit_size}{byte_suffix}'

file_size_re = re.compile(r'^(?P<value>[0-9\.,]+?)\s*(?P<unit_size>[KMGTPEZY]{0,1})(?P<byte_suffix>i{0,1}B{1})?$', re.IGNORECASE)
FILESIZE_UNITS_BINARY = {
    '': 1,
    'K': 1 << 10,
    'M': 1 << 20,
    'G': 1 << 30,
    'T': 1 << 40,
    'P': 1 << 50,
    'E': 1 << 60,
    'Z': 1 << 70,
    'Y': 1 << 80,
}
FILESIZE_UNITS_DECIMAL = {
    '': 1,
    'K': 1 * (10 ** 3),
    'M': 1 * (10 ** 6),
    'G': 1 * (10 ** 9),
    'T': 1 * (10 ** 12),
    'P': 1 * (10 ** 15),
    'E': 1 * (10 ** 18),
    'Z': 1 * (10 ** 21),
    'Y': 1 * (10 ** 24),
}


def filesizeformat(bytes, decimals=1, binary=True, ambiguous_suffix=True):
    """
    Formats the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 bytes, etc).
    Based on django.template.defaultfilters.filesizeformat
    """

    try:
        bytes = float(bytes)
    except (TypeError, ValueError, UnicodeDecodeError):
        raise ValueError

    filesize_number_format = lambda value: formats.number_format(round(value, decimals), decimals)

    filesize_units = FILESIZE_UNITS_DECIMAL
    byte_suffix = DEFAULT_BYTE_SUFFIX

    if binary:
        filesize_units = FILESIZE_UNITS_BINARY
        if not ambiguous_suffix:
            byte_suffix = BINARY_BYTE_SUFFIX

    units_list = sorted(six.iteritems(filesize_units), key=operator.itemgetter(1))

    value = unit_size = None
    len_unints_list = len(units_list)
    for i in xrange(1, len_unints_list):
        if bytes < units_list[i][1]:
            prev_unit = units_list[i - 1]
            value = filesize_number_format(bytes / prev_unit[1])
            unit_size = prev_unit[0]
            break

    if value is None:
        value = filesize_number_format(bytes / units_list[-1][1])
        unit_size = units_list[-1][0]

    unit = UNIT_FORMAT.format(unit_size=unit_size, byte_suffix=byte_suffix)
    return SIZEFIELD_FORMAT.format(value=value, unit=unit)


def parse_size(size, assume_binary=True):
    """
    @rtype int
    """
    if isinstance(size, six.integer_types):
        return size

    r = file_size_re.match(size)
    if r:
        unit_size = r.group('unit_size').upper() or ''
        byte_suffix = r.group('byte_suffix') or ''

        if byte_suffix != '' or unit_size == '':
            clean_value = r.group("value").replace(",", ".")
            value = float(clean_value)

            file_size_units = FILESIZE_UNITS_BINARY
            if not assume_binary and byte_suffix.upper() != BINARY_BYTE_SUFFIX.upper():
                file_size_units = FILESIZE_UNITS_DECIMAL

            return int(value * file_size_units[unit_size])

    # Regex pattern was not matched
    raise ValueError(_("Size '%s' has incorrect format") % size)
