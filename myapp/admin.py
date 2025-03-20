from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'verification_token', 'is_email_verified')
    def username(self, obj):
        return obj.user.username
    search_fields = ('user__username', 'user__email')
admin.site.register(UserProfile, UserProfileAdmin)


class OpenSpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'district', 'created_at', 'is_active')
admin.site.register(OpenSpace, OpenSpaceAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id','description', 'space_name', 'email', 'file', 'created_at', 'latitude', 'longitude')
admin.site.register(Report, ReportAdmin)

class ReportHistoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'email', 'file_path', 'confirmed_at')
admin.site.register(ReportHistory, ReportHistoryAdmin)