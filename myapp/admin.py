from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'verification_token', 'is_email_verified')
    def username(self, obj):
        return obj.user.username
    search_fields = ('user__username', 'user__email')
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']
