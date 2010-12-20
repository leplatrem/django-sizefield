from django import forms

from sizefield import render_size


class FileSizeWidget(forms.TextInput):
    
    def render(self, name, value, attrs=None):
        value = render_size(value)
        return super(FileSizeWidget, self).render(name, value, attrs)
