from django.contrib import admin
from openspace.myapprest.models import UssdReport

# Register your models here.
class UssdReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'description', 'submitted_at')
admin.site.register(UssdReport, UssdReportAdmin)