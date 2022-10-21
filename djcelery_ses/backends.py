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
        CHUNK_SIZE = getattr(settings, "DJCELERY_SES_CHUNK_SIZE", 50)

        pages, remainder = divmod(len(email_messages), CHUNK_SIZE)
        if remainder != 0:
            pages += 1

        for page in range(pages):
            offset = CHUNK_SIZE * page
            email_messages_chunk = email_messages[offset: offset + CHUNK_SIZE]

            if NO_DELAY:
                send_emails(email_messages_chunk, **kwargs)
            else:
                send_emails.delay(email_messages_chunk, **kwargs)

        return len(email_messages)
