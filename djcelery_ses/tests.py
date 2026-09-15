import os.path
from smtplib import SMTPDataError
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.core import mail
from django.core.mail import EmailMessage
from django.test.utils import override_settings

from .models import Blacklist, MessageLog
from .tasks import send_emails
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

    @override_settings(DJCELERY_SES_CHECK_BLACKLIST=False)
    def test_not_check_blacklist_setting(self):
        # Add `noreply@example.com` to Blacklist
        Blacklist.objects.create(email='noreply@example.com', type=0)

        # Send email to `noreply@example.com`
        msg = EmailMessage('title', 'body content', 'noreply@example.com', ['noreply@example.com'])
        msg.send()

        # should be one email in outbox, since blacklist check is disabled
        self.assertEqual(len(mail.outbox), 1)


class SendEmailsTaskErrorTest(TestCase):
    @patch('djcelery_ses.tasks.get_connection')
    def test_smtp_data_error_554_blacklists_recipient(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_conn.send_messages.side_effect = SMTPDataError(554, b'Message rejected')
        mock_get_connection.return_value = mock_conn

        recipient = 'bounce@example.com'
        msg = EmailMessage('title', 'body content', 'noreply@example.com', [recipient])
        send_emails([msg])

        self.assertTrue(Blacklist.objects.filter(email=recipient).exists())
        self.assertEqual(
            MessageLog.objects.filter(email=recipient, result='3').count(), 1)

    @patch('djcelery_ses.tasks.get_connection')
    def test_smtp_data_error_554_existing_blacklist_entry_does_not_raise(
            self, mock_get_connection):
        recipient = 'bounce@example.com'
        Blacklist.objects.create(email=recipient, type=0)

        mock_conn = MagicMock()
        mock_conn.send_messages.side_effect = SMTPDataError(554, b'Message rejected')
        mock_get_connection.return_value = mock_conn

        msg = EmailMessage('title', 'body content', 'noreply@example.com', [recipient])
        send_emails([msg])

        self.assertEqual(Blacklist.objects.filter(email=recipient).count(), 1)

    @patch('djcelery_ses.tasks.get_connection')
    def test_smtp_data_error_other_code_does_not_blacklist(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_conn.send_messages.side_effect = SMTPDataError(451, b'Temporary failure')
        mock_get_connection.return_value = mock_conn

        recipient = 'temp@example.com'
        msg = EmailMessage('title', 'body content', 'noreply@example.com', [recipient])
        send_emails([msg])

        self.assertFalse(Blacklist.objects.filter(email=recipient).exists())
        self.assertEqual(MessageLog.objects.filter(email=recipient).count(), 0)

    @patch('djcelery_ses.tasks.get_connection')
    @patch('djcelery_ses.tasks.send_emails.retry')
    def test_generic_exception_single_message_retries(
            self, mock_retry, mock_get_connection):
        recipient = 'fail@example.com'
        exc = RuntimeError('boom')

        mock_conn = MagicMock()
        mock_conn.send_messages.side_effect = exc
        mock_get_connection.return_value = mock_conn

        msg = EmailMessage('title', 'body content', 'noreply@example.com', [recipient])
        send_emails([msg])

        mock_retry.assert_called_once_with(exc=exc)
        self.assertEqual(
            MessageLog.objects.filter(email=recipient, result='2').count(), 1)

    @patch('djcelery_ses.tasks.get_connection')
    @patch('djcelery_ses.tasks.send_emails.delay')
    def test_generic_exception_batch_redelays_failed_message(
            self, mock_delay, mock_get_connection):
        mock_conn = MagicMock()
        mock_conn.send_messages.side_effect = RuntimeError('boom')
        mock_get_connection.return_value = mock_conn

        msg1 = EmailMessage(
            'title', 'body content', 'noreply@example.com', ['fail@example.com'])
        msg2 = EmailMessage(
            'title', 'body content', 'noreply@example.com', ['fail2@example.com'])
        send_emails([msg1, msg2])

        self.assertEqual(mock_delay.call_count, 2)
        mock_delay.assert_any_call([msg1])
        mock_delay.assert_any_call([msg2])
        self.assertEqual(MessageLog.objects.filter(result='2').count(), 2)


class SNSNotificationTest(TestCase):
    urls = 'djcelery_ses.urls'

    def test_notification(self):
        PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIRS = os.path.join(PROJECT_ROOT, 'fixtures')

        with open(os.path.join(FIXTURE_DIRS, 'sns.json')) as f:
            content = f.read()

        self.client.post('/sns_notification/', content, content_type="application/json")

        self.assertEqual(Blacklist.objects.count(), 1)
        self.assertEqual(Blacklist.objects.get().type, 0)

    def test_complaint_notification(self):
        PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIRS = os.path.join(PROJECT_ROOT, 'fixtures')

        with open(os.path.join(FIXTURE_DIRS, 'complaint.json')) as f:
            content = f.read()

        self.client.post('/sns_notification/', content, content_type="application/json")

        self.assertEqual(Blacklist.objects.count(), 1)
        blacklist_entry = Blacklist.objects.get()
        self.assertEqual(blacklist_entry.email, 'complaint@example.com')
        self.assertEqual(blacklist_entry.type, 1)

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
