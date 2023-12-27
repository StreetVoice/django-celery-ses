from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.test.runner import DiscoverRunner

from celery import current_app


USAGE = """\
Custom test runner to allow testing of celery delayed tasks.
"""


def _set_eager():
    settings.task_always_eager = True
    current_app.conf.task_always_eager = True
    settings.task_eager_propagates = True  # Issue #75
    current_app.conf.task_eager_propagates = True

def _set_pickle():
    settings.task_serializer="pickle"
    current_app.conf.task_serializer="pickle"
    settings.accept_content=["pickle", "json"]
    current_app.conf.accept_content=["pickle", "json"]


class CeleryTestSuiteRunner(DiscoverRunner):
    """Django test runner allowing testing of celery delayed tasks.

    All tasks are run locally, not in a worker.

    To use this runner set ``settings.TEST_RUNNER``::

        TEST_RUNNER = 'djcelery_ses.test_runner.CeleryTestSuiteRunner'

    """
    def setup_test_environment(self, **kwargs):
        _set_eager()
        _set_pickle()
        super().setup_test_environment(**kwargs)
