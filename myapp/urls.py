from django.urls import path
from .views import *


urlpatterns = [
    path('api/reports/reply/', ReplyToReportAPIView.as_view(), name='reply-to-report'),
]
