from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UssdReport(models.Model):
    reference_number = models.CharField(max_length=8, unique=True, default="unknown")
    phone_number = models.CharField(max_length=255)  # Increased size to store encrypted phone number
    open_space = models.CharField(max_length=255, default='Unknown')  # Add default value here
    description = models.TextField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.reference_number

