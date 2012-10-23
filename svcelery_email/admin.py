from django.contrib import admin
from svcelery_email.models import Blacklist, MessageLog

admin.site.register(Blacklist)
admin.site.register(MessageLog)
