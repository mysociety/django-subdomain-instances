from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from .fields import DNSLabelField


class InstanceManager(models.Manager):
    def for_instance(self, instance):
        return self.get_query_set().filter(instance=instance)


@python_2_unicode_compatible
class Instance(models.Model):
    label = DNSLabelField(db_index=True, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='instances',
        blank=True,
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_instances',
        null=True,
        blank=True,
        )

    def __str__(self):
        return u'Instance %s' % self.label

    def get_absolute_url(self):
        url = 'http://%s.%s' % (
            self.label,
            getattr(settings, 'BASE_HOST', '127.0.0.1.xip.io'),
            )
        if getattr(settings, 'BASE_PORT', None):
            url += ':%s' % settings.BASE_PORT
        return url


class InstanceMixin(models.Model):
    instance = models.ForeignKey(Instance)

    objects = InstanceManager()

    class Meta:
        abstract = True
