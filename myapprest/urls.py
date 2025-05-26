from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('ussd/', views.submit_problem_report, name='ussd'),
    path('confirm-report/<int:pk>/', views.confirm_report, name='confirm_report'),
    path('reference-ussd/<str:reference_number>/', get_report_status, name='get_report_status'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('upload-profile-image/', ProfileImageUploadView.as_view(), name='upload-profile-image'),
    path('password-reset/', SendResetPasswordEmailView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('book-open-space/', OpenSpaceBookingView.as_view(), name='book-open-space'),
    path('district-bookings/', DistrictBookingsAPIView.as_view(), name='district-bookings'),
    path('accept-and-forward-booking/<int:booking_id>/', views.accept_and_forward_booking, name='accept-and-forward-booking'),
]
