from django.conf import settings
from django.db import IntegrityError
from django.core.mail import get_connection
from svcelery_email.models import Blacklist, MessageLog
from smtplib import SMTPDataError
from celery.task import task

BACKEND = getattr(settings, 'CELERY_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')

@task(ignore_result=True)
def send_email(message, **kwargs):
    logger = send_email.get_logger()
    conn = get_connection(backend=BACKEND)

    # check blacklist
    try:
        Blacklist.objects.get(email=message.to[0])
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
    except SMTPDataError, e:
        logger.warning("Message to %r, blacklisted.", message.to)
        if e.smtp_code == 554:
            MessageLog.objects.log(message, 3)
            try:
                Blacklist(email=message.to[0]).save()
            except IntegrityError:
                pass
    except Exception, e:
        MessageLog.objects.log(message, 2)
        logger.warning("Failed to send email message to %r, retrying.", message.to)
        send_email.retry(exc=e)

    conn.close()
