from openspace.myapp.models import Report
from .models import *
from rest_framework import serializers

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fiels = ['file']