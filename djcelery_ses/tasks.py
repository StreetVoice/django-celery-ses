from smtplib import SMTPDataError

from django.conf import settings
from django.db import IntegrityError
from django.core.mail import get_connection

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Blacklist, MessageLog

logger = get_task_logger(__name__)


CONFIG = getattr(settings, 'CELERY_EMAIL_TASK_CONFIG', {})
BACKEND = getattr(settings, 'CELERY_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')

TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': True,
}
TASK_CONFIG.update(CONFIG)


@shared_task(**TASK_CONFIG)
def send_emails(messages, **kwargs):
    """
    send mails task
    """
    conn = get_connection(backend=BACKEND)
    conn.open()

    num = 0
    for message in messages:
        # check blacklist
        CHECK_BLACKLIST = getattr(
            settings, 'DJCELERY_SES_CHECK_BLACKLIST', True)
        if CHECK_BLACKLIST:
            logger.debug('Check blacklist')

            try:
                Blacklist.objects.get(email=message.to[0], type=0)
                logger.debug("Email already in blacklist.")
                continue
            except Blacklist.DoesNotExist:
                pass

        # send
        try:
            result = conn.send_messages([message])
            logger.debug("Successfully sent email message to %r.", message.to)
            MessageLog.objects.log(message, 1)
            num += result
        except SMTPDataError as e:
            logger.warning("Message to %r, blacklisted.", message.to)
            if e.smtp_code == 554:
                MessageLog.objects.log(message, 3)
                try:
                    Blacklist(email=message.to[0]).save()
                except IntegrityError:
                    pass
        except Exception as e:
            MessageLog.objects.log(message, 2)
            logger.warning(
                "Failed to send email message to %r, retrying.", message.to)
            if len(messages) == 1:
                send_emails.retry(exc=e)
            else:
                send_emails.delay([message], **kwargs)

    conn.close()
    return num
