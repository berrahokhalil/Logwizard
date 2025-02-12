from django.contrib import admin
from .models import User, LogFiles, Logs, Notifications

# Register your models here.
class LogsAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'priority', 'code', 'OS', 'browser')
    search_fields = ('name', 'priority', 'OS', 'browser')
    list_filter = ('priority', 'OS', 'browser', 'code')


admin.site.register(User)
admin.site.register(LogFiles)
admin.site.register(Logs, LogsAdmin)
admin.site.register(Notifications)
