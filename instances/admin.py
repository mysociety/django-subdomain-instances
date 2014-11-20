from django.contrib import admin

from .models import Instance


class InstanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Instance, InstanceAdmin)
