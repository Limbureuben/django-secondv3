from django.db import models

# Create your models here.
class Registration(models.Model):
    name = models.CharField(max_length=200)
    email= models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    passwordConfirm = models.CharField(max_length=200)

class Login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)