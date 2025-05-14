from django.db import models
from django.contrib.auth.models import AbstractUser
from myapp.models import *
from django.utils import timezone
from datetime import timedelta
import re
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


class OpenSpaceBooking(models.Model):
    open_space = models.ForeignKey('OpenSpace', on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    duration = models.CharField(max_length=50)  # e.g., '2 hours', '30 minutes'
    purpose = models.TextField()
    file = models.FileField(upload_to='ward_executive_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.username} - {self.open_space.name} - {self.datetime}"

    def calculate_end_time(self):
        """Parses the duration field to compute end_time from datetime."""
        duration_lower = self.duration.lower()
        hours = minutes = 0

        hour_match = re.search(r'(\d+)\s*hour', duration_lower)
        minute_match = re.search(r'(\d+)\s*minute', duration_lower)

        if hour_match:
            hours = int(hour_match.group(1))
        if minute_match:
            minutes = int(minute_match.group(1))

        return self.datetime + timedelta(hours=hours, minutes=minutes)
