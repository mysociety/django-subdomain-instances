from django.test import TestCase, LiveServerTestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.validators import ValidationError
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, HttpResponse

try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    pass

from .models import Instance
from .middleware import MultiInstanceMiddleware

FAKE_URL = 'testing.example.org:8000'


class InstanceClient(Client):
    def __init__(self, enforce_csrf_checks=False, **defaults):
        defaults.setdefault('HTTP_HOST', FAKE_URL)
        super(InstanceClient, self).__init__(
            enforce_csrf_checks=enforce_csrf_checks, **defaults)


@override_settings(
    BASE_HOST='example.org',
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
)
class InstanceTestCase(TestCase):
    client_class = InstanceClient

    # Override in a subclass if you need to change what the default instance
    # created looks like.
    default_instance_options = dict(label='testing', title="Test Instance")

    def setUp(self):
        self.instance = Instance.objects.create(**self.default_instance_options)
        user = User.objects.create_user(
            username='admin', email='admin@example.org', password='admin')
        user.instances.add(self.instance)
        self.client.login(username='admin', password='admin')


@override_settings(SESSION_COOKIE_DOMAIN='127.0.0.1.nip.io')
class InstanceLiveServerTestCase(LiveServerTestCase):
    # Override in a subclass if you need to change what the default instance
    # created looks like.
    default_instance_options = dict(label='testing', title="Test Instance")

    def setUp(self):
        self.instance = Instance.objects.create(**self.default_instance_options)
        user = User.objects.create_user(
            username='admin', email='admin@example.org', password='admin')
        user.instances.add(self.instance)

        self.selenium.get(
            '%s%s' % (self.live_server_url, '/accounts/login/?next=/'))
        username_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()


# ---

class SimpleTest(TestCase):
    def test_instance_lower_casing(self):
        i = Instance(label='HELLO')
        self.assertEqual(i.label, 'hello')

    def test_bad_label(self):
        self.assertRaises(
            ValidationError, lambda: Instance(label='Spaces are not allowed'))
        self.assertRaises(
            ValidationError, lambda: Instance(label='Nor-a-symbol-such-as-^'))
        self.assertRaises(
            ValidationError, lambda: Instance(label="Nor-can-you-end-with--"))


class MiddlewareTest(TestCase):
    def setUp(self):
        self.middleware = MultiInstanceMiddleware(lambda request: HttpResponse('hey'))
        self.request = HttpRequest()
        self.request.META = {
            'SERVER_PORT': '80',
        }

    def test_no_match(self):
        self.request.META['SERVER_NAME'] = 'localhost'
        response = self.middleware(self.request)
        self.assertEqual(response['Vary'], 'Host')
        self.assertEqual(self.request.instance, None)
        self.assertEqual(self.request.urlconf, 'instances.urls')
        self.assertEqual(response.content, b'hey')

    def test_bad_instance(self):
        self.request.META['SERVER_NAME'] = 'testing.127.0.0.1.nip.io'
        response = self.middleware(self.request)
        self.assertEqual(response['Vary'], 'Host')
        self.assertEqual(response['Location'], 'http://127.0.0.1.nip.io')

    def test_good_instance(self):
        self.request.META['SERVER_NAME'] = 'testing.127.0.0.1.nip.io'
        self.instance = Instance.objects.create(label='testing')
        self.request.user = AnonymousUser()
        response = self.middleware(self.request)
        self.assertEqual(response['Vary'], 'Host')
        self.assertEqual(self.request.instance, self.instance)
        self.assertEqual(self.request.is_user_instance, False)

    def test_good_user_instance(self):
        self.request.META['SERVER_NAME'] = 'testing.127.0.0.1.nip.io'
        self.instance = Instance.objects.create(label='testing')
        user = User.objects.create_user(
            username='admin', email='admin@example.org', password='admin')
        user.instances.add(self.instance)
        self.request.user = user
        response = self.middleware(self.request)
        self.assertEqual(response['Vary'], 'Host')
        self.assertEqual(self.request.instance, self.instance)
        self.assertEqual(self.request.is_user_instance, True)
