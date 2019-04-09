import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.cache import patch_vary_headers

from .models import Instance


def MultiInstanceMiddleware(get_response):
    """
    Check for a hostname of the form <instance>.BASE_HOST, or <instance>.127.0.0.1.nip.io;
    if not given, use ROOT_URLCONF_HOST or instances.urls as the urlconf. If given, check
    if it exists in the database; if not, redirect to BASE_HOST, if it does,
    set request.instance and check if the logged in user has access to it
    """
    def process_request(self, request):
        host = request.get_host().lower()
        domain = getattr(settings, 'BASE_HOST', '127.0.0.1.nip.io')
        pattern = r'^(?P<instance>.*?)\.%s(?::(?P<port>.*))?$' % re.escape(domain)
        matches = re.match(pattern, host)
        if not matches:
            request.instance = None
            request.urlconf = getattr(settings, 'ROOT_URLCONF_HOST', 'instances.urls')
            return

        try:
            request.instance = Instance.objects.get(label=matches.group('instance'))
        except Instance.DoesNotExist:
            url = '%(scheme)s://%(domain)s' % {
                'scheme': 'https' if request.is_secure() else 'http',
                'domain': domain,
                }
            if matches.group('port'):
                url += ':' + matches.group('port')
            return HttpResponseRedirect(url)

        request.is_user_instance = request.user.is_authenticated() and (
            request.instance in request.user.instances.all() or request.user.is_superuser)

    def middleware(request):
        response = process_request(request)
        if not response:
            response = get_response(request)
        patch_vary_headers(response, ('Host',))
        return response

    return middleware
