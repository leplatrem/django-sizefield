from __future__ import unicode_literals

import re
import operator

from django.utils import formats
from django.utils import six
from django.utils.translation import ugettext as _
from django.conf import settings


SIZEFIELD_FORMAT = getattr(settings, 'SIZEFIELD_FORMAT', '{value}{unit}')

SIZEFIELD_IS_BINARY = getattr(settings, 'SIZEFIELD_IS_BINARY', True)
SIZEFIELD_AMBIGUOUS_SUFFIX = getattr(settings, 'SIZEFIELD_AMBIGUOUS_SUFFIX', True)
SIZEFIELD_ASSUME_BINARY = getattr(settings, 'SIZEFIELD_ASSUME_BINARY', SIZEFIELD_IS_BINARY and SIZEFIELD_AMBIGUOUS_SUFFIX)

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


def filesizeformat(bytes, decimals=1, is_binary=None, ambiguous_suffix=None):
    """
    Formats the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 bytes, etc). By default, the value is assumed to be binary with an
    ambiguous suffix (as opposed to 13 KiB, 4.1 MiB, 102 B, etc).
    Based on django.template.defaultfilters.filesizeformat
    """

    if is_binary == None:
        is_binary = SIZEFIELD_IS_BINARY
    if ambiguous_suffix == None:
        ambiguous_suffix = SIZEFIELD_AMBIGUOUS_SUFFIX

    try:
        bytes = float(bytes)
    except (TypeError, ValueError, UnicodeDecodeError):
        raise ValueError

    filesize_number_format = lambda value: formats.number_format(round(value, decimals), decimals)

    filesize_units = FILESIZE_UNITS_DECIMAL
    byte_suffix = DEFAULT_BYTE_SUFFIX

    if is_binary:
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

    # If the unit is only iB, use B instead
    if unit_size == '':
        byte_suffix = DEFAULT_BYTE_SUFFIX

    unit = UNIT_FORMAT.format(unit_size=unit_size, byte_suffix=byte_suffix)
    return SIZEFIELD_FORMAT.format(value=value, unit=unit)


def parse_size(size, assume_binary=None):
    """
    @rtype int
    """
    if isinstance(size, six.integer_types):
        return size

    if assume_binary == None:
        assume_binary = SIZEFIELD_ASSUME_BINARY

    r = file_size_re.match(size)
    if r:
        unit_size = r.group('unit_size').upper() or ''
        byte_suffix = r.group('byte_suffix') or ''

        if byte_suffix != '' or unit_size == '':
            clean_value = r.group("value").replace(",", ".")
            value = float(clean_value)

            # Decide whether to parse as a binary or decimal size
            file_size_units = FILESIZE_UNITS_BINARY
            if not assume_binary and byte_suffix.upper() != BINARY_BYTE_SUFFIX.upper():
                file_size_units = FILESIZE_UNITS_DECIMAL

            return int(value * file_size_units[unit_size])

    # Regex pattern was not matched
    raise ValueError(_("Size '%s' has incorrect format") % size)
