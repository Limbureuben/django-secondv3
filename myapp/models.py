from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Registration(models.Model):
    name = models.CharField(max_length=200)
    email= models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    passwordConfirm = models.CharField(max_length=200)

class Login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"
