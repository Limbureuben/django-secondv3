from django.contrib import admin
from .models import *

admin.site.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']

admin.site.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']
