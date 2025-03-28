from django.contrib import admin
from .models import *

# Register your models here.
class UssdReportAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'open_space', 'description', 'status')
admin.site.register(UssdReport, UssdReportAdmin)