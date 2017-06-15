import re

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy

label_re = re.compile(r'(?i)^[a-z0-9][a-z0-9-]*[a-z0-9]$')
validate_label = RegexValidator(
    label_re, ugettext_lazy("Enter a valid instance label consisting of letters, numbers, or hyphens."), 'invalid')


class Creator(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class DNSLabelField(models.CharField):
    description = "A DNS label"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 63)
        super(DNSLabelField, self).__init__(*args, **kwargs)
        self.validators.append(validate_label)

    def contribute_to_class(self, cls, name):
        super(DNSLabelField, self).contribute_to_class(cls, name)
        setattr(cls, name, Creator(self))

    def to_python(self, value):
        value = super(DNSLabelField, self).to_python(value)
        if value == '' or value is None:
            return value
        # Want immediate validation on any instance creation
        validate_label(value)
        return value.lower()
