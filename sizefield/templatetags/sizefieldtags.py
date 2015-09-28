from django import template

from sizefield.utils import filesizeformat


register = template.Library()


@register.filter(name='filesize')
def filesize(value, decimals=1):
    if value is None:
        return ''
    return filesizeformat(value, decimals)


@register.simple_tag(name='custom_filesize')
def custom_filesize(value, decimals=1, is_binary=True, ambiguous_suffix=True):
    if value is None:
        return ''
    return filesizeformat(value, decimals=decimals, is_binary=is_binary, ambiguous_suffix=ambiguous_suffix)
