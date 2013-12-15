from django.test import TestCase
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.test.utils import override_settings

from .models import Blacklist
from .utils import pass_blacklist


@override_settings(
    EMAIL_BACKEND='djcelery_ses.backends.CeleryEmailBackend',
    CELERY_EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
)
class DjcelerySESTest(TestCase):
    def test_send_mail(self):
        msg = EmailMessage('title', 'body content', 'noreply@example.com', ['noreply@example.com'])
        msg.send()

        self.assertEqual(len(mail.outbox), 1)

    def test_blacklist(self):
        # Add `noreply@example.com` to Blacklist
        Blacklist.objects.create(email='noreply@example.com', type=0)
        
        # Send email to `noreply@example.com`
        msg = EmailMessage('title', 'body content', 'noreply@example.com', ['noreply@example.com'])
        msg.send()

        # should be no email in outbox
        self.assertEqual(len(mail.outbox), 0)

    def test_pass_blacklist(self):
         # Add `noreply@example.com` to Blacklist
        Blacklist.objects.create(email='noreply@example.com', type=0)
        
        # Send email to `noreply@example.com`
        with pass_blacklist:
            msg = EmailMessage('title', 'body content', 'noreply@example.com', ['noreply@example.com'])
            msg.send()

        # should be no email in outbox
        self.assertEqual(len(mail.outbox), 1)
