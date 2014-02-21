from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

from .tasks import send_email


class CeleryEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super(CeleryEmailBackend, self).__init__(fail_silently)
        self.init_kwargs = kwargs

    def send_messages(self, email_messages, **kwargs):
        results = []
        kwargs['_backend_init_kwargs'] = self.init_kwargs
        for msg in email_messages:
            NO_DELAY = getattr(settings, 'DJCELERY_SES_NO_DELAY', False)
            if NO_DELAY:
                result = send_email(msg, **kwargs)
            else:
                result = send_email.delay(msg, **kwargs)
            results.append(result)
        return results
