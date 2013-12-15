#!/usr/bin/env python

import sys
from os.path import dirname, abspath

from django.conf import settings


settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'djcelery',
        'djcelery_ses',
    ],
    SITE_ID=1,
    DEBUG=False,
    CELERY_EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
)



def runtests(**test_args):
    from django.test.utils import get_runner

    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['djcelery_ses'], test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
