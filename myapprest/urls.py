from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('ussd/', views.submit_problem_report, name='ussd'),
    path('confirm-report/', views.confirm_report, name='confirm_report'),
]
