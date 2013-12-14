from django.contrib import admin
from svcelery_email.models import Blacklist, MessageLog

admin.site.register(Blacklist)

class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'result', 'created_at')
admin.site.register(MessageLog, MessageLogAdmin)
