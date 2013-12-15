from django.contrib import admin
from .models import Blacklist, MessageLog

class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('email', 'type', 'created_at')
    list_filter = ('type',)
admin.site.register(Blacklist, BlacklistAdmin)


class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'result', 'created_at')
admin.site.register(MessageLog, MessageLogAdmin)
