Instances
=========

A simple way of allowing subdomains to be served by the same project, and
associating objects with particular subdomains.

Installation
------------

1. By default, it will work if you use 127.0.0.1.nip.io (a domain that points
   to localhost) on port 80. To use a different base domain/port, set the
   `BASE_HOST` and/or `BASE_PORT` variables.

2. Add `instances` to your `INSTALLED_APPS` and migrate to get the Instance
   database table.

3. Add Instance objects, with the label being the subdomain you wish to use.
   Optionally, associate users with these instances.

4. Add `instances.middleware.MultiInstanceMiddleware` to your middleware; it
   must come after AuthenticationMiddleware. Now
   if you go to `<subdomain>.<BASE_HOST>`, request.instance will be set to the
   matching Instance object. If there's a subdomain given but no match, it will
   redirect to `BASE_HOST`.

Requests to a subdomain will use your `ROOT_URLCONF` file; requests to the
`BASE_HOST` will use `ROOT_URLCONF_HOST` or `instances.urls` by default (which
just has one page that lists all instances)..

Instance edit form
------------------

In your ROOT_URLCONF, use a line like the following to have a page for editing
the title and description of an instance:

`url(r'^instance/edit$', InstanceUpdate.as_view(), name='instance-edit')`

Associating models
------------------

To have a model's objects be associated with an instance, mix in InstanceMixin,
and if you have a custom manager make it a subclass of InstanceManager. This
adds an `instance` field, and provides a `for_instance` manager method to
return all the objects in the given instance.

Mix in InstanceViewMixin to any display class-based view to restrict the
default queryset to the request's instance. Add InstanceFormMixin to any
create/update view to store the current instance upon save, and allow editing
only by those users associated with the instance. Remember to exclude
`instance` from any model form, as it won't be seen.

Running tests
-------------

.. code-block::

    pip install .
    python runtests.py
