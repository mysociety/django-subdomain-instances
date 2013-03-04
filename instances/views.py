class InstanceViewMixin(object):
    def get_queryset(self):
        return self.model.objects.for_instance(self.request.instance)

class InstanceFormMixin(InstanceViewMixin):
    def form_valid(self, form):
        # If not present, fill in the instance from the request
        # Clash of naming two things 'instance' here, sorry.
        if hasattr(form, 'instance') and not hasattr(form.instance, 'instance'):
            form.instance.instance = self.request.instance
        return super(InstanceFormMixin, self).form_valid(form)

