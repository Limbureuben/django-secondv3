from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']
