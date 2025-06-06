from django.urls import path
from .views import *


urlpatterns = [
     path('api/confirm-report/', confirm_report),
]
