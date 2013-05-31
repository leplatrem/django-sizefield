import re
from decimal import Decimal, getcontext

from django.utils.translation import ugettext as _


FILESIZE_UNITS = {
    _('B') : 2**10, 
    _('KB'): 2**20, 
    _('MB'): 2**30, 
    _('GB'): 2**40, 
    _('TB'): 2**50,
    _('PB'): 2**60,
}


def render_size(value, decimals=1):
    """
    @rtype string
    """
    suffixes = sorted(FILESIZE_UNITS.items(), cmp=lambda x,y: cmp(x[1],y[1]))
    try:
        value = int(value)
    except ValueError:
        # check if value already pretty !
        value = parse_size(value)  # Will raise ValueError if incorrect format

    for suf, lim in suffixes:
        if value >= lim:
            continue
        else:
            value = Decimal(value) / (lim / 2**10)
            value = value.quantize(Decimal(10)**-decimals)  # 10^-n precision.
            return "%(value)s%(suf)s" % locals()


def parse_size(txt):
    """
    @rtype int
    """
    if isinstance(txt, (int,long)):
        return txt
    p = re.compile(r'^(?P<value>[0-9\.]+?)\s*(?P<unit>(B{0,1}|[KMGT]{1}B{1})?)$')
    r = p.match(txt)
    if r:
        value = float(r.group('value'))  # Will raise ValueError if incorrect format
        unit  = r.group('unit') or _('B')
        multi = FILESIZE_UNITS[unit]  # should never fail.
        return int(value * multi/2**10)
    # Regex pattern was not matched
    raise ValueError(_("Size '%s' has incorrect format") % txt)
