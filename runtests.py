import sys

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        ROOT_URLCONF='instances.urls',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'instances',
        ),
        MIDDLEWARE_CLASSES=(),
    )
    if hasattr(django, 'setup'):  # Django 1.7
        django.setup()

if __name__ == '__main__':
    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(failfast=False)
    failures = runner.run_tests(['instances'])
    sys.exit(failures)
