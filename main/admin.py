from django.contrib import admin
from .models import Macro, MacroFeeLog, MacroLog, UserPage, Board


class MacroAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'detail', 'user', 'modified', 'created')
    list_filter = ('modified',)
    readonly_fields = ('title', 'id', 'detail', 'user', 'modified', 'created')
    search_fields = ( 'user__username', 'title', 'id')


class MacroLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'macro', 'ip', 'created')
    list_filter = ('created',)
    readonly_fields = ('user', 'macro', 'ip', 'created')
    search_fields = ('user__username', 'macro__title', 'ip')


class UserPageAdmin(admin.ModelAdmin):
    list_display = ('user', 'macro', 'end_date', 'end_yn')
    list_filter = ('modified',)
    readonly_fields = ('user', 'macro')
    search_fields = ('user__username', 'macro__title')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'detail', 'user', 'count', 'ip', 'created', 'modified')
    list_filter = ('modified',)
    search_fields = ('id', 'user__username', 'title', 'detail', 'ip')


admin.site.register(Macro, MacroAdmin)
admin.site.register(UserPage, UserPageAdmin)
admin.site.register(MacroFeeLog)
admin.site.register(MacroLog, MacroLogAdmin)
admin.site.register(Board, BoardAdmin)