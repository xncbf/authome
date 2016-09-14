from django.contrib import admin
from .models import Macro, MacroFeeLog, MacroLog, UserPage


# Register your models here.

admin.site.register(Macro)
admin.site.register(UserPage)
admin.site.register(MacroFeeLog)
admin.site.register(MacroLog)
