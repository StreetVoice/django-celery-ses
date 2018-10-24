import os.path

from django.test import TestCase
from django.core import mail
from django.core.mail import EmailMessage
from django.test.utils import override_settings

from .models import Blacklist
from .utils import pass_blacklist, no_delay


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

        # should be one email in outbox
        self.assertEqual(len(mail.outbox), 1)

    def test_no_delay(self):
        with no_delay: 
            msg = EmailMessage('title', 'body content', 'noreply@example.com', ['noreply@example.com'])
            msg.send()
            
        self.assertEqual(len(mail.outbox), 1)

class SNSNotificationTest(TestCase):
    urls = 'djcelery_ses.urls'

    def test_notification(self):
        PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIRS = os.path.join(PROJECT_ROOT, 'fixtures')

        with open(os.path.join(FIXTURE_DIRS, 'sns.json')) as f:
            content = f.read()

        self.client.post('/sns_notification/', content, content_type="application/json")

        self.assertEqual(Blacklist.objects.count(), 1)

    def test_error_notification(self):
        resp = self.client.post('/sns_notification/', 'hello', content_type="application/json")
        self.assertEqual(resp.content.decode(), 'Invalid JSON')
        self.assertEqual(resp.status_code, 400)


    def test_subscription(self):
        PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIRS = os.path.join(PROJECT_ROOT, 'fixtures')

        with open(os.path.join(FIXTURE_DIRS, 'subscription.json')) as f:
            content = f.read()

        self.client.post('/sns_notification/', content, content_type="application/json")

