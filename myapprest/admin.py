from django.contrib import admin
from .models import *

# Register your models here.
class UssdReportAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'open_space', 'description', 'status', 'phone_number')
admin.site.register(UssdReport, UssdReportAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')  # Add 'is_active' to display
    search_fields = ('username', 'email')  # You can search by username or email
    list_filter = ('role', 'is_active')  # Add 'is_active' filter to the sidebar
    list_editable = ('is_active',)  # Allows admins to toggle 'is_active' from the list view
admin.site.register(CustomUser, CustomUserAdmin)

class OpenSpaceBookingAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact', 'duration', 'space')
admin.site.register(OpenSpaceBooking, OpenSpaceBookingAdmin)