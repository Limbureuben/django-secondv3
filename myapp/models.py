import random
import string
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
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
    
# class Report(models.Model):
#     report_id = models.CharField(max_length=10, unique=True, blank=True)
#     description = models.TextField()
#     email = models.EmailField()
#     file = models.FileField(upload_to='uploads/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"Report {self.report_id}"
    
#     def save(self, *args, **kwargs):
#         if not self.report_id:  # Generate only if it's not already set
#             self.report_id = self.generate_report_id()
#         super().save(*args, **kwargs)

#     def generate_report_id(self, length=8):
#         """Generate a unique alphanumeric report ID."""
#         while True:
#             report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
#             if not Report.objects.filter(report_id=report_id).exists():  # Ensure uniqueness
#                 return report_id

#     def __str__(self):
#         return f"Report {self.report_id}"



class Report(models.Model):
    report_id = models.CharField(max_length=8, unique=True, editable=False)
    description = models.TextField()
    email = models.EmailField(blank=True, null=True)  # Optional email field
    file = models.FileField(upload_to='reports/', blank=True, null=True)  # Optional file field
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add new fields for openspace details
    space_name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate unique ID if not already set
        is_new = not self.pk
        if not self.report_id:
            self.report_id = self._generate_unique_id()
        super().save(*args, **kwargs)
        # Send email notification if email is provided and it's a new report
        if is_new and self.email:
            self._send_notification_email()

    def _generate_unique_id(self):
        # Generate a unique 8-character ID
        unique_id = uuid.uuid4().hex[:8].upper()
        # Check if ID already exists, if so, generate a new one
        while Report.objects.filter(report_id=unique_id).exists():
            unique_id = uuid.uuid4().hex[:8].upper()
        return unique_id

    def _send_notification_email(self):
        subject = f'Your Report #{self.report_id} has been received'
        message = f'''
        Thank you for submitting your report.
        Report ID: {self.report_id}
        Submission Date: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        Location: {self.space_name if self.space_name else "Not specified"}
        We have received your report and will process it shortly.
        This is an automated message, please do not reply.
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )