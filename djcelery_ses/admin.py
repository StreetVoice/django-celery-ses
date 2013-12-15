from django.contrib import admin
from svcelery_email.models import Blacklist, MessageLog

class BlacklistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blacklist, BlacklistAdmin)

class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'result', 'created_at')
admin.site.register(MessageLog, MessageLogAdmin)
