from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .fields import DNSLabelField


class InstanceManager(models.Manager):
    def for_instance(self, instance):
        return self.get_query_set().filter(instance=instance)


@python_2_unicode_compatible
class Instance(models.Model):
    label = DNSLabelField(_('label'), db_index=True, unique=True)
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    users = models.ManyToManyField(
        User, verbose_name=_('users'), related_name='instances', blank=True)
    created_by = models.ForeignKey(
        User, verbose_name=_('created by'), related_name='created_instances',
        null=True, blank=True)

    class Meta:
        verbose_name = _('instance')
        verbose_name_plural = _('instances')

    def __str__(self):
        return u'Instance %s' % self.label

    def get_absolute_url(self):
        url = 'http://%s.%s' % (self.label, getattr(settings, 'BASE_HOST', '127.0.0.1.xip.io'))
        if getattr(settings, 'BASE_PORT', None):
            url += ':%s' % settings.BASE_PORT
        return url


class InstanceMixin(models.Model):
    instance = models.ForeignKey(Instance, verbose_name=_('instance'))

    objects = InstanceManager()

    class Meta:
        abstract = True
