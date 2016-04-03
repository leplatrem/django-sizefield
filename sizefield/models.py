from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from sizefield.utils import parse_size
from sizefield.utils import SIZEFIELD_IS_BINARY
from sizefield.widgets import FileSizeWidget


class FileSizeField(models.BigIntegerField):

    default_error_messages = {
        'invalid': _(u'Incorrect file size format.'),
    }

    def __init__(self, is_binary=None, ambiguous_suffix=None, assume_binary=None, *args, **kwargs):
        self.is_binary = is_binary
        self.ambiguous_suffix = ambiguous_suffix

        self.assume_binary = assume_binary
        if assume_binary == None:
            # Binary fields are always assumed to be binary when parsed
            self.assume_binary = is_binary
            if is_binary == None:
                self.assume_binary = SIZEFIELD_IS_BINARY

        super(FileSizeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = FileSizeWidget(is_binary=self.is_binary, ambiguous_suffix=self.ambiguous_suffix, assume_binary=self.assume_binary)
        kwargs['error_messages'] = self.default_error_messages
        return super(FileSizeField, self).formfield(**kwargs)

    def to_python(self, value):
        if value is None:
            return None
        try:
            return parse_size(value, assume_binary=self.assume_binary)
        except ValueError:
            raise exceptions.ValidationError(self.error_messages['invalid'])

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^sizefield\.models\.FileSizeField"])
except ImportError:
    pass
