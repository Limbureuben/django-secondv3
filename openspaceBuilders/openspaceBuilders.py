from openspace.openspace_dto.Response import *
from django.contrib.auth.models import User

# class register_user:
#     def __init__(self, input):
#         self.username = input.username
#         self.email = input.email
#         self.password = input.password
#         self.passwordConfirm = input.passwordConfirm

#     def validate_password(self):
#         if self.password != self.passwordConfirm:
#             return RegistrationResponse(message="Passwords do not match", success=False)


def register_user(input):
    username = input.username,
    email = input.email,
    password = input.password,
    passwordConfirm = input.passwordConfirm

    if password != passwordConfirm:
        return RegistrationResponse(message="Passwords do not match", success=False)
    
    if len(password) < 8:
        return RegistrationResponse(message="Password must be atleast 8 characters long", success=False)
     
    user = User.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    return RegistrationResponse(message="User registred successfully", success=True)