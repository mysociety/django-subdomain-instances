import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.cache import patch_vary_headers

from .models import Instance

class MultiInstanceMiddleware:
    def process_request(self, request):
        host = request.get_host().lower()
        domain = getattr(settings, 'BASE_HOST', '127.0.0.1.xip.io')
        pattern = r'^(?P<instance>.*?)\.%s(?::(?P<port>.*))?$' % re.escape(domain)
        matches = re.match(pattern, host)
        if not matches:
            request.instance = None
            request.urlconf = getattr(settings, 'ROOT_URLCONF_HOST', 'instances.urls')
            return

        try:
            request.instance = Instance.objects.get(label=matches.group('instance'))
        except:
            url = 'http://' + domain
            if matches.group('port'):
                url += ':' + matches.group('port')
            return HttpResponseRedirect(url)

    def process_response(self, request, response):
        patch_vary_headers(response, ('Host',))
        return response
