from django.db import models


class Blacklist(models.Model):
    TYPE_CHOICES = (
        (0, 'Bounce'),
        (1, 'Complaints'),
    )
    email = models.EmailField(unique=True)
    type = models.PositiveSmallIntegerField(default=0, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email


RESULT_CODES = (
    ("1", "success"),
    ("2", "retry"),
    ("3", "blacklisted"),
)

class MessageLogManager(models.Manager):
    def log(self, message, result_code):
        subject = message.subject[:250] + '...' if len(message.subject) > 255 else message.subject
        self.create(email=message.to[0], subject=subject, result=result_code)
        

class MessageLog(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    result = models.CharField(max_length=1, choices=RESULT_CODES)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MessageLogManager()

    def __unicode__(self):
        return self.email
