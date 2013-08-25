from django import template

from sizefield.utils import filesizeformat


register = template.Library()


@register.filter(name='filesize')
def filesize(value, decimals=1):
    return filesizeformat(value, decimals)
