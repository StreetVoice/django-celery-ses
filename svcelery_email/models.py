from django.db import models


class Blacklist(models.Model):
    email = models.EmailField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


RESULT_CODES = (
    ("1", "success"),
    ("2", "retry"),
    ("3", "blacklisted"),
)

class MessageLogManager(models.Manager):
    def log(self, message, result_code):
        self.create(email=message.to, body=message.message(), result=result_code)
        

class MessageLog(models.Model):
    email = models.EmailField()
    body = models.TextField()
    result = models.CharField(max_length=1, choices=RESULT_CODES)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MessageLogManager()
