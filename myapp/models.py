from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"


class Login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)