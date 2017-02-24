from smtplib import SMTPDataError

from django.conf import settings
from django.db import IntegrityError
from django.core.mail import get_connection

from celery.task import task

from .models import Blacklist, MessageLog


CONFIG = getattr(settings, 'CELERY_EMAIL_TASK_CONFIG', {})
BACKEND = getattr(settings, 'CELERY_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')

TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': True,
}
TASK_CONFIG.update(CONFIG)


@task(**TASK_CONFIG)
def send_email(message, **kwargs):
    """
    send mail task
    """

    logger = send_email.get_logger()
    conn = get_connection(backend=BACKEND)

    # check blacklist
    CHECK_BLACKLIST = getattr(settings, 'DJCELERY_SES_CHECK_BLACKLIST', True)
    if CHECK_BLACKLIST:
        logger.debug('Check blacklist')

        try:
            Blacklist.objects.get(email=message.to[0], type=0)
            logger.debug("Email already in blacklist.")
            return
        except Blacklist.DoesNotExist:
            pass

    # send
    try:
        result = conn.send_messages([message])
        logger.debug("Successfully sent email message to %r.", message.to)
        MessageLog.objects.log(message, 1)
        return result
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
        logger.warning("Failed to send email message to %r, retrying.", message.to)
        send_email.retry(exc=e)

    conn.close()
