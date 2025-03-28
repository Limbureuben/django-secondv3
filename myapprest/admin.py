from django.contrib import admin
from .models import *

# Register your models here.
class UssdReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'description', 'submitted_at')
admin.site.register(UssdReport, UssdReportAdmin)