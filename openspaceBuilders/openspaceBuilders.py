from openspace_dto.Response import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.conf import settings
from django.http import HttpResponse
from myapp.models import *
from myapp.tasks import send_verification_email

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
    
def register_user(input):
    try:
        user = UserBuilder.register_user(input.username, input.email, input.password, input.passwordConfirm)
        return RegistrationResponse(message="Registration successful. Please check your email to verify your account", success=True)
    except ValidationError as e:
        return RegistrationResponse(message=str(e), success=False)
    

# class UserBuilder:
#     @staticmethod
#     def register_user(username, email, password, password_confirm):
#         if password != password_confirm:
#             raise ValidationError("Password do not match")
        
#         user = User(username=username, email=email)
#         user.set_password(password)
#         user.save()
#         return user