from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'verification_token', 'is_email_verified')
    def username(self, obj):
        return obj.user.username
    search_fields = ('user__username', 'user__email')
admin.site.register(UserProfile, UserProfileAdmin)


class OpenSpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'district')
admin.site.register(OpenSpace, OpenSpaceAdmin)