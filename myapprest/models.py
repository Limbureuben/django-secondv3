from django.db import models

# Create your models here.
class UssdReport(models.Model):
    reference_number = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15)
    open_space = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='Pending')
    
    def __str__(self):
        return f"Report {self.reference_number} by {self.phone_number}"