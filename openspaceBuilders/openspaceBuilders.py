
from myapp.tasks import send_verification_email
from openspace_dto.openspace import *
from openspace_dto.Response import RegistrationResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserBuilder:
    @staticmethod
    def register_user(username, email, password, passwordConfirm):
        if password != passwordConfirm:
            raise ValidationError("Passwords do not match")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already taken")
        
        user = User(username=username, email=email)
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        user_profile = UserProfile(user=user, verification_token=uuid.uuid4())
        user_profile.save()

        verification_url = f"{settings.BACKEND_URL}/verify-email/{user_profile.verification_token}/"
        send_verification_email.delay(email, verification_url)
        
        return user
    
    @staticmethod
    def login_user(username, password):
        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError("Invalid username or password")

        # Ensure the user has a profile
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise ValidationError("User profile not found. Please contact support.")

        # Check if email is verified
        if not user_profile.is_email_verified:
            raise ValidationError("Email not verified. Please check your inbox for a verification link.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
           
            "access_token": str(refresh.access_token),
        }



class UserProfileBuilder:
    
    @staticmethod
    def create_user_profile(user: User) ->UserProfileObject:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }


def register_user(input):
    try:
        user = UserBuilder.register_user(input.username, input.email, input.password, input.passwordConfirm)

        return RegistrationResponse(
            message="Registration successful.Please verify your email",
            success=True,
            user=RegistrationObject(id=str(user.id), username=user.username, email=user.email)
        )
    except ValidationError as e:
        return RegistrationResponse(message=str(e), success=False, user=None)
