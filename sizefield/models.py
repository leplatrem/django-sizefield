from django.db import models
from django import forms
from django.core import exceptions
from django.utils.translation import ugettext as _

from sizefield import parse_size
from sizefield.widgets import FileSizeWidget


class FileSizeField(models.BigIntegerField):

    default_error_messages = {
        'invalid': _(u'Incorrect file size format.'),
    }

    def formfield(self, **kwargs):
        kwargs['widget'] = FileSizeWidget
        kwargs['form_class'] = forms.CharField
        #return super(FileSizeField, self).formfield(**defaults)  # Fails :/ because of max_value/min_value
        return  models.Field.formfield(self, **kwargs)

    def to_python(self, value):
        try:
            return parse_size(value)
        except ValueError:
            raise exceptions.ValidationError(self.error_messages['invalid'])


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^sizefield\.models\.FileSizeField"])
except ImportError:
    pass
