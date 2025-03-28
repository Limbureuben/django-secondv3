from django.db import models

# Create your models here.
class UssdReport(models.Model):
    phone_number = models.CharField(max_length=15)
    description = models.TextField()
    report_id = models.CharField(max_length=50, unique=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.report_id