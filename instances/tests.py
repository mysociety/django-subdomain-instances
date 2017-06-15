from django.test import TestCase, LiveServerTestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.validators import ValidationError
from django.contrib.auth.models import User

try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    pass

from .models import Instance

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

    def assertRedirects(self, *args, **kwargs):
        kwargs['host'] = FAKE_URL
        return super(InstanceTestCase, self).assertRedirects(*args, **kwargs)


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
