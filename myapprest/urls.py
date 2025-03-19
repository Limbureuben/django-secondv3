from .views import *
from django.urls import path

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
