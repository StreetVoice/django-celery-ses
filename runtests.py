#!/usr/bin/env python

import sys
from os.path import dirname, abspath

from django.conf import settings
import django

settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    MIDDLEWARE=(
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ),
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "OPTIONS": {
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            }
        }
    ],
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        "django.contrib.messages",
        'djcelery_ses',
    ],
    SITE_ID=1,
    DEBUG=False,
    ROOT_URLCONF='djcelery_ses.urls',
    CELERY_EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    TEST_RUNNER='djcelery_ses.test_runner.CeleryTestSuiteRunner',
    SECRET_KEY='secret',
)



def runtests(**test_args):
    from django.test.utils import get_runner
    django.setup()

    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['djcelery_ses'], test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
