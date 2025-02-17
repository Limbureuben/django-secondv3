from openspace.openspace_dto.Response import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.conf import settings
from django.http import HttpResponse
from myapp.models import *

# class register_user:
#     def __init__(self, input):
#         self.username = input.username
#         self.email = input.email
#         self.password = input.password
#         self.passwordConfirm = input.passwordConfirm

#     def validate_password(self):
#         if self.password != self.passwordConfirm:
#             return RegistrationResponse(message="Passwords do not match", success=False)

class UserBuilder:
    @staticmethod
    def register_user(username, email, password, passwordConfirm):

        if password != passwordConfirm:
            raise ValidationError("Passwords do not match")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        return RegistrationResponse(message="User registred successfully", success=True)