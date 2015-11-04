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
    django.setup()

if __name__ == '__main__':
    from django.test.runner import DiscoverRunner
    runner = DiscoverRunner(failfast=False)
    failures = runner.run_tests(['instances'])
    sys.exit(failures)
