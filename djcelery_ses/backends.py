# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from .tasks import send_emails


class CeleryEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super(CeleryEmailBackend, self).__init__(fail_silently)
        self.init_kwargs = kwargs

    def send_messages(self, email_messages, **kwargs):
        if not email_messages:
            return 0

        kwargs["_backend_init_kwargs"] = self.init_kwargs

        NO_DELAY = getattr(settings, "DJCELERY_SES_NO_DELAY", False)
        if NO_DELAY:
            send_emails(email_messages, **kwargs)
        else:
            send_emails.delay(email_messages, **kwargs)
        return len(email_messages)
