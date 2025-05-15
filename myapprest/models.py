from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta, datetime
import re
from myapp.models import OpenSpace
from django.core.exceptions import ValidationError

# Create your models here.
class UssdReport(models.Model):
    reference_number = models.CharField(max_length=8, unique=True, default="unknown")
    phone_number = models.CharField(max_length=255)  # Increased size to store encrypted phone number
    open_space = models.CharField(max_length=255, default='Unknown')  # Add default value here
    description = models.TextField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.reference_number
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('ward_executive', 'Ward Executive'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    ward = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"


# class OpenSpaceBooking(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='open_space_bookings')
#     open_space = models.ForeignKey(OpenSpace, on_delete=models.CASCADE)
#     username = models.CharField(max_length=100)
#     contact = models.CharField(max_length=20)
#     date = models.DateField(blank=True, default=timezone.now)  # changed from DateTimeField to DateField
#     duration = models.CharField(max_length=50)  # e.g., '2 hours', '30 minutes'
#     purpose = models.TextField()
#     file = models.FileField(upload_to='ward_executive_files/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.username} - {self.open_space.name} - {self.date}"


class OpenSpaceBooking(models.Model):
    username = models.CharField(max_length=150)
    contact = models.CharField(max_length=20)
    date = models.DateField()
    duration = models.CharField(max_length=50)
    purpose = models.TextField()
    file = models.FileField(upload_to='bookings/files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.date}"