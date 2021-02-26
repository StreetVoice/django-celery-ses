from django.contrib import admin
from .models import Blacklist, MessageLog

class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('email', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('email',)
admin.site.register(Blacklist, BlacklistAdmin)


class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'result', 'created_at')
    search_fields = ('email',)
admin.site.register(MessageLog, MessageLogAdmin)
