
import random
import string
from myapp.tasks import send_verification_email
from openspace_dto.openspace import *
from openspace_dto.Response import OpenspaceResponse, RegistrationResponse, ReportResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail


class UserBuilder:
    VALID_DISTRICTS = {"Kinondoni", "Ilala", "Ubungo", "Temeke", "Kigamboni"}
    @staticmethod
    def register_user(username, password, passwordConfirm):
        if password != passwordConfirm:
            raise ValidationError("Passwords do not match")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken")
        
        user = User(username=username)
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        # user_profile = UserProfile(user=user, verification_token=uuid.uuid4())
        # user_profile.save()

        # verification_url = f"{settings.BACKEND_URL}/verify-email/{user_profile.verification_token}/"
        # send_verification_email.delay(email, verification_url)
        
        return user
    
    
        
    @staticmethod
    def login_user(username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Invalid username or password")
        
        refresh = RefreshToken.for_user(user)
        
        # Return a dictionary with the access token, refresh token, and the user object
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user,
        }
        
    @staticmethod    
    def generate_report_id(length=8):
        """Generate a unique alphanumeric report ID."""
        while True:
            report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Report.objects.filter(report_id=report_id).exists():  # Ensure uniqueness
                return report_id
        
    @staticmethod
    def report_issue(description, email=None):
        if len(description) < 20:
            raise ValidationError("Description must be at least 20 characters long")

        # Generate unique report ID
        report_id = UserBuilder.generate_report_id()

        # Save the report to the database
        report = Report(description=description, email=email, report_id=report_id)
        report.save()

        # Send email notification if the user provided an email
        if email:
            if "@" not in email:
                raise ValidationError("Invalid email")

            email_subject = f"Issue Report Received - Report ID: {report_id}"
            email_body = (
                f"Thank you for reporting an issue. Your report ID is: {report_id}.\n\n"
                f"Description:\n{description}\n\n"
                "Our team will review your report as soon as possible. Thank you for helping us improve our environment."
            )

            send_mail(
                subject=email_subject,
                message=email_body,
                from_email='limbureubenn@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

        return report

    # @staticmethod
    # def request_password_reset(email):
    #     try:
    #         user = User.objects.get(email=email)
    #         reset_token = uuid.uuid4()
    #         user_profile = user.userprofile
    #         user_profile.reset_token = reset_token
    #         user_profile.save()

    #         reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_token}/"
    #         send_mail(
    #             'Password Reset Request',
    #             f'Please click the following link to reset your password: { reset_url}',
    #             'no-reply@example.com',
    #             [email],
    #             fail_silently=False
    #         )
    #         return True
    #     except User.DoesNotExist:
    #         raise ValidationError("User with this email does not exist")
        
    # @staticmethod
    # def reset_password(token, new_password, new_password_confirm):
    #     try:
    #         user_profile = UserProfile.objects.get(reset_token=token)
    #         if new_password != new_password_confirm:
    #             raise ValidationError("Passoword do not match")
    #         if len(new_password) < 8:
    #             raise ValidationError("Password must be atleast 8 characters long")
    #         user = user_profile.user
    #         user.set_password(new_password)
    #         user.save()
    #         user_profile.reset_token = None
    #         user_profile.save()
    #         return True
    #     except UserProfile.DoesNotExist:
    #         raise ValidationError("Invalid reset token")
    
   
    @staticmethod
    def open_space(name, latitude, longitude, district):
        if district not in UserBuilder.VALID_DISTRICTS:
            raise ValueError(f"Invalid district: {district}. Must be one of {', '.join(UserBuilder.VALID_DISTRICTS)}")
        openspace=OpenSpace(name=name, latitude=latitude, longitude=longitude, district=district, is_active=True)
        openspace.save()
        return openspace


def register_user(input):
    try:
        user = UserBuilder.register_user(input.username, input.password, input.passwordConfirm)

        return RegistrationResponse(
            message="User registration successful",
            success=True,
            user=RegistrationObject(id=str(user.id), username=user.username)
        )
    except ValidationError as e:
        return RegistrationResponse(message=str(e), success=False, user=None)

def open_space(input):
    try:
        openspace = UserBuilder.open_space(input.name, input.latitude, input.longitude, input.district)
        return OpenspaceResponse(
            message = "Openspace registred successfully",
            success=True,
            openspace=OpenspaceObject(name=openspace.name, latitude=openspace.latitude, longitude=openspace.longitude)
        )
    except ValidationError as e:
        return OpenspaceResponse(message=str(e), success=False, openspace=None)
    
def report_issue(input):
    try:
        report = UserBuilder.report_issue(input.description, input.email)
        return ReportResponse(
            message = "Report submitted successfully",
            success=True,
            report=ReportObject(description=report.description, email=report.email)
        )
    except ValidationError as e:
        return ReportResponse(message=str(e), success=False, report=None)