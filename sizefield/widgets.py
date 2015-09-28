from django import forms
from django.core.validators import EMPTY_VALUES

from sizefield.utils import filesizeformat, parse_size


class FileSizeWidget(forms.TextInput):

    def __init__(self, attrs=None, is_binary=None, ambiguous_suffix=None, assume_binary=None):
        self.attrs = attrs or {}

        self.is_binary = is_binary
        self.ambiguous_suffix = ambiguous_suffix
        self.assume_binary = assume_binary

    def render(self, name, value, attrs=None):
        if value:
            try:
                value = filesizeformat(value, is_binary=self.is_binary, ambiguous_suffix=self.ambiguous_suffix)
            except ValueError:
                pass
        return super(FileSizeWidget, self).render(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        value = super(FileSizeWidget, self).value_from_datadict(data, files, name)
        if value not in EMPTY_VALUES:
            try:
                return parse_size(value, assume_binary=self.assume_binary)
            except ValueError:
                pass
        return value
