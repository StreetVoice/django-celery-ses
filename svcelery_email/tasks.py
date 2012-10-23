from django.conf import settings
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
        Blacklist.objects.get(email=message.to)
        logger.debug("Email already in blacklist.")
    except Blacklist.DoesNotExist:
        pass

    # send
    try:
        result = conn.send_messages([message])
        logger.debug("Successfully sent email message to %r.", message.to)
        return result
    except SMTPDataError, e:
        logger.warning("message to %r, blacklisted.", message.to)
        if e.smtp_code == 554:
            Blacklist(email=message.to).save()
    except Exception, e:
        logger.warning("Failed to send email message to %r, retrying.", message.to)
        send_email.retry(exc=e)

    MessageLog.objects.log(message)

    conn.close()
