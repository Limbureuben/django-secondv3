from myapp.models import Report
from .models import *
from rest_framework import serializers # type: ignore

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        
        
class ProblemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UssdReport
        fields = ['id', 'phone_number', 'open_space', 'description', 'reference_number', 'status']