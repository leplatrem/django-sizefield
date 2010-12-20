from django import template

from sizefield import render_size


register = template.Library()

@register.filter(name='filesize')
def filesize(value, decimals=1):
    return render_size(value, decimals)
