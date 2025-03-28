from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('submit_report/', views.submit_problem_report, name='submit_report'),
]
