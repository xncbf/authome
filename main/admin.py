from django.contrib import admin
from django_ses.views import dashboard
from .models import Macro, MacroFeeLog, MacroLog, UserPage


class MacroAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'detail', 'user', 'modified', 'created')
    list_filter = ('modified',)
    readonly_fields = ('title', 'id', 'detail', 'user', 'modified', 'created')
    search_fields = ('title', 'id', 'detail', 'user')


class MacroLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'macro', 'ip', 'created')
    list_filter = ('created',)
    readonly_fields = ('user', 'macro', 'ip', 'created')
    search_fields = ('user', 'macro', 'ip', 'created')


class UserPageAdmin(admin.ModelAdmin):
    list_display = ('user', 'macro', 'end_date', 'end_yn')
    list_filter = ('modified',)
    readonly_fields = ('user', 'macro')
    search_fields = ('user', 'macro', 'end_date', 'end_yn')


admin.site.register(Macro, MacroAdmin)
admin.site.register(UserPage, UserPageAdmin)
admin.site.register(MacroFeeLog)
admin.site.register(MacroLog, MacroLogAdmin)
admin.site.register_view('django-ses', dashboard, 'Django SES Stats')