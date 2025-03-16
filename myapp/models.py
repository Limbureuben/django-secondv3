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
    
    def __str__(self):
        return self.name
    