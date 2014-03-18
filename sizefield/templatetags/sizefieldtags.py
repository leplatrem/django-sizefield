from django import template

from sizefield.utils import filesizeformat


register = template.Library()


@register.filter(name='filesize')
def filesize(value, decimals=1):
    if value is None:
        return ''
    return filesizeformat(value, decimals)
