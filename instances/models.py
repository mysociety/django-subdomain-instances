from django.db import models
from .fields import DNSLabelField

class InstanceManager(models.Manager):
    def for_instance(self, instance):
        return self.get_query_set().filter(instance=instance)

class Instance(models.Model):
    label = DNSLabelField( db_index=True, unique=True )

class InstanceMixin(models.Model):
    instance = models.ForeignKey(Instance)

    objects = InstanceManager()

    class Meta:
        abstract = True

