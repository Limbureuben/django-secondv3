import random
import string
from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_email_verified = models.BooleanField(default=False)  # Track if email is verified

    def __str__(self):
        return f"{self.user.username} Profile"

class OpenSpace(models.Model):
    DISTRICT_CHOICES = [
        ('Kinondoni', 'Kinondoni'),
        ('Ilala', 'Ilala'),
        ('Ubungo', 'Ubungo'),
        ('Temeke', 'Temeke'),
        ('Kigamboni', 'Kigamboni'),
    ]
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Report(models.Model):
    report_id = models.CharField(max_length=10, unique=True, blank=True)
    description = models.TextField()
    email = models.EmailField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report {self.report_id}"
    
    def save(self, *args, **kwargs):
        if not self.report_id:  # Generate only if it's not already set
            self.report_id = self.generate_report_id()
        super().save(*args, **kwargs)

    def generate_report_id(self, length=8):
        """Generate a unique alphanumeric report ID."""
        while True:
            report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Report.objects.filter(report_id=report_id).exists():  # Ensure uniqueness
                return report_id

    def __str__(self):
        return f"Report {self.report_id}"
