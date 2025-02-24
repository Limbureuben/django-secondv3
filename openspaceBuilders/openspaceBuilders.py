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
    def register_user(username, email, password, password_confirm):
        if password != password_confirm:
            raise ValidationError("Password do not match")
        
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
    
    @staticmethod
    def login_user(username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Invalid username or password')

    # Check if the user's email is verified unless they are a superuser
        if user.is_superuser and not UserProfile.is_email_verified:
            print('pass')
            raise ValidationError('Email not verified')

    # Create tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }


class UserProfileBuilder:
    
    @staticmethod
    def create_user_profile(user: User) ->UserProfileObject:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }


# def register_user(input):
#     try:
#         user = UserBuilder.register_user(input.username, input.email, input.password, input.passwordConfirm)

#         return RegistrationResponse(
#             message="Registration successful. Please check your email to verify your account",
#             success=True,
#             user=RegistrationObject(id=str(user.id), username=user.username, email=user.email)
#         )
#     except ValidationError as e:
#         return RegistrationResponse(message=str(e), success=False, user=None)
