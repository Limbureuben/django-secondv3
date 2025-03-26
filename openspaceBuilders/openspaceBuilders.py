
import random
import string
from tokenize import TokenError

from graphql import GraphQLError
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
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

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
    # In your login mutation or view
    def login_user(username, password):
        try:
            # Authenticate and generate tokens
            user = authenticate(username=username, password=password)
            
            if user:
                # Print detailed user information
                # print(f"Authenticated User Details:")
                # print(f"Username: {user.username}")
                # print(f"User ID: {user.id}")
                # print(f"Is Staff: {user.is_staff}")
                
                # Generate and print tokens
                refresh = RefreshToken.for_user(user)
                # print(f"Access Token: {str(refresh.access_token)}")
                # print(f"Refresh Token: {str(refresh)}")
                return {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user,
                    }
            
            # Rest of your login logic
        except Exception as e:
            print(f"Login Error: {str(e)}")
    
        
    # @staticmethod
    # def login_user(username, password):
    #     user = authenticate(username=username, password=password)
    #     if user is None:
    #         raise ValidationError("Invalid username or password")
        
    #     refresh = RefreshToken.for_user(user)
        
    #     # Return a dictionary with the access token, refresh token, and the user object
    #     return {
    #         "refresh": str(refresh),
    #         "access": str(refresh.access_token),
    #         "user": user,
    #     }
        
    # @staticmethod    
    # def generate_report_id(length=8):
    #     """Generate a unique alphanumeric report ID."""
    #     while True:
    #         report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    #         if not Report.objects.filter(report_id=report_id).exists():  # Ensure uniqueness
    #             return report_id
    @staticmethod
    def get_user_profile_data(user):
        try:
            # Retrieve UserProfile for the authenticated user
            user_profile = UserProfile.objects.get(user=user)
            print(user_profile)
        except UserProfile.DoesNotExist:
            raise GraphQLError("Profile not found")
        data=ProfileObject(
            id=user_profile.id,
            user=UserObject(
                pk=user.pk,
                username=user_profile.user.username,
                is_staff=user_profile.user.is_staff
            )
        )
        print(data)
        return data
        
        
    @staticmethod    
    def report_issue(description, email=None, file_url=None):
        if len(description) < 5:
            raise ValidationError("Description must be at least 20 characters long")

        # Create and save the report (report_id is auto-generated)
        report = Report(description=description, email=email)
        
        if file_url:
            report.file = file_url  

        report.save()

        # Send email notification if the user provided an email
        if email:
            if "@" not in email:
                raise ValidationError("Invalid email")

            email_subject = f"Issue Report Received - Report ID: {report.report_id}"
            email_body = (
                f"Thank you for reporting an issue. Your report ID is: {report.report_id}.\n\n"
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
    
    def get_report_history(user):
        reports=ReportHistory.objects.filter(user=user)
        print(reports)
        all_reports=[]
        for report in reports:
            report_data=HistoryObject(
                reportId=report.report_id,
                description=report.description,
                created_at=report.created_at      
            )
            all_reports.append(report_data)
        return all_reports
    


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
        
        if hasattr(input, 'sessionId') and input.sessionId:
            Report.objects.filter(submitted_by=input.sessionId).update(submitted_by=user.id)

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
        report = UserBuilder.report_issue(input.description, input.email, input.file_url)
        return ReportResponse(
            message="Report submitted successfully",
            success=True,
            report=ReportObject(
                description=report.description, 
                email=report.email, 
                id=report.report_id,  # FIXED: Include report ID in response
                file_url=report.file.url if report.file else None  # FIXED: Provide correct file URL if exists
            )
        )
    except ValidationError as e:
        return ReportResponse(message=str(e), success=False, report=None)









from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

class AuthenticationDebugger:
    @staticmethod
    def verify_token_user(token):
        """
        Verify the user associated with a given token
        """
        try:
            # Decode the access token
            decoded_token = AccessToken(token)
            
            # Extract user ID from token
            user_id = decoded_token['user_id']
            
            # Retrieve the user
            User = get_user_model()
            user = User.objects.get(id=user_id)
            
            return {
                'user_id': user.id,
                'username': user.username,
                'is_staff': user.is_staff,
                'token_valid': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'token_valid': False
            }

    @staticmethod
    def debug_login_process(username, password):
        """
        Comprehensive login process debugging
        """
        try:
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is None:
                return {
                    'success': False,
                    'error': 'Authentication failed'
                }
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return {
                'success': True,
                'user_details': {
                    'id': user.id,
                    'username': user.username,
                    'is_staff': user.is_staff
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Usage example
def login_and_verify(username, password):
    # Debug login process
    login_result = AuthenticationDebugger.debug_login_process(username, password)
    
    if login_result['success']:
        # Verify the generated token
        token_verification = AuthenticationDebugger.verify_token_user(
            login_result['tokens']['access']
        )
        
        return {
            'login_details': login_result,
            'token_verification': token_verification
        }
    
    return login_result




class TokenSecurityInvestigator:
    @staticmethod
    def investigate_token_discrepancy(token):
        """
        Comprehensive investigation of token authentication issues
        """
        User = get_user_model()
        
        try:
            # Decode the token
            decoded_token = AccessToken(token)
            
            # Extract user ID from token
            token_user_id = decoded_token.get('user_id')
            
            # print("Token Investigation Results:")
            # print(f"Token User ID: {token_user_id}")
            
            # Retrieve the user associated with the token
            try:
                token_user = User.objects.get(id=token_user_id)
                # print(f"Token User Details:")
                # print(f"Username: {token_user.username}")
                # print(f"Is Active: {token_user.is_active}")
            except User.DoesNotExist:
                print(f"No user found with ID {token_user_id}")
            
            # Check for potential user context manipulation
            all_active_users = User.objects.filter(is_active=True)
            print("\nActive Users:")
            for user in all_active_users:
                print(f"ID: {user.id}, Username: {user.username}")
            
        except (TokenError, InvalidToken) as e:
            print(f"Token Validation Error: {str(e)}")
        except Exception as e:
            print(f"Unexpected Error during token investigation: {str(e)}")

# Middleware or Authentication Backend Investigation
class AuthenticationContextInvestigator:
    @staticmethod
    def debug_authentication_context(request):
        """
        Investigate authentication context and middleware
        """
        print("\nAuthentication Context Debug:")
        
        # Check user authentication
        user = request.user
        if user.is_authenticated:
            print(f"Authenticated User: {user.username}")
            print(f"User ID: {user.id}")
        else:
            print("No authenticated user found")
        
        # Inspect authentication headers
        print("\nAuthentication Headers:")
        for key, value in request.META.items():
            if 'AUTH' in key.upper():
                print(f"{key}: {value}")
        
        # Check session details
        if hasattr(request, 'session'):
            print("\nSession Details:")
            for key, value in request.session.items():
                print(f"{key}: {value}")

# Usage Example
def investigate_authentication_issue(access_token):
    print("Starting Token Security Investigation")
    TokenSecurityInvestigator.investigate_token_discrepancy(access_token)