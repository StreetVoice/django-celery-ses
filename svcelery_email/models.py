from django.db import models
from datetime import datetime


class Blacklist(models.Model):
    email = models.EmailField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


RESULT_CODES = (
    ("1", "success"),
    ("2", "don't send"),
    ("3", "failure"),
)

PRIORITIES = (
    ("1", "high"),
    ("2", "medium"),
    ("3", "low"),
    ("4", "deferred"),
)

class MessageLogManager(models.Manager):

    def log(self, message, result_code, log_message=""):
        """
        create a log entry for an attempt to send the given message and
        record the given result and (optionally) a log message
        """

        return self.create(
            message_data = message.message_data,
            when_added = message.when_added,
            priority = message.priority,
            # @@@ other fields from Message
            result = result_code,
            log_message = log_message,
        )

class MessageLog(models.Model):
    # fields from Message
    message_data = models.TextField()
    when_added = models.DateTimeField()
    priority = models.CharField(max_length=4, choices=PRIORITIES)
    # @@@ campaign?

    # additional logging fields
    when_attempted = models.DateTimeField(default=datetime.now)
    result = models.CharField(max_length=1, choices=RESULT_CODES)
    log_message = models.TextField()

    objects = MessageLogManager()
