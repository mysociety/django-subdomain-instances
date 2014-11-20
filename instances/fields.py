import re

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy
from django.utils.six import with_metaclass

label_re = re.compile(r'(?i)^[a-z0-9][a-z0-9-]*[a-z0-9]$')
validate_label = RegexValidator(
    label_re, ugettext_lazy("Enter a valid instance label consisting of letters, numbers, or hyphens."), 'invalid')

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^instances\.fields\.DNSLabelField"])
except ImportError:
    pass


class DNSLabelField(with_metaclass(models.SubfieldBase, models.CharField)):
    description = "A DNS label"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 63)
        super(DNSLabelField, self).__init__(*args, **kwargs)
        self.validators.append(validate_label)

    def to_python(self, value):
        value = super(DNSLabelField, self).to_python(value)
        if value == '' or value is None:
            return value
        # Want immediate validation on any instance creation
        validate_label(value)
        return value.lower()
