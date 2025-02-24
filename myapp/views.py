import uuid
from django.conf import settings
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import graphene # type: ignore
from .tasks import send_verification_email # type: ignore
from .models import *
from openspaceBuilders.openspaceBuilders import UserBuilder, register_user
from openspace_dto.openspace import *
from openspace_dto.Response import RegistrationResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# class RegisterUser(graphene.Mutation):
#     user = graphene.Field(RegistrationObject)
#     success = graphene.Boolean()
#     message = graphene.String()
    
#     class Arguments:
#         input = RegistrationInputObject(required=True)
        
#     def mutate(self, info, input):
#         username = input.username
#         email = input.email
#         password = input.password
#         passwordConfirm = input.passwordConfirm
        
#         ##check if the user exist
#         if User.objects.filter(username=username).exists():
#             return RegisterUser(success=False, message="username alredy exists")
        
#         ##check if the email exist
#         if User.objects.filter(email=email).exists():
#             return RegisterUser(success=False, message="Email alredy exists")
        
#         if password != passwordConfirm:
#             return RegisterUser(success=False, message="Passwords do not match")
        
#         user = User(username=username, email=email)
#         user.set_password(password)
#         user.is_superuser = False
#         user.is_staff = False
#         user.save()
        
#         user_profile = UserProfile(user=user, verification_token=uuid.uuid4())
#         user_profile.save()
#         print("Token are created here")
        
#         # Generate verification URL
#         # verification_url = f"{settings.FRONTEND_URL}/verify-email/{user_profile.verification_token}/"
#         verification_url = f"{settings.BACKEND_URL}/verify-email/{user_profile.verification_token}/"

#         print("Token can also pass here 2")
#         # Call Celery task
#         send_verification_email.delay(email, verification_url)
        
#         return RegisterUser(
#             user=RegistrationObject(id=user.id, username=user.username, email=user.email),
#             success=True,
#             message="Registration successful. Please check your email to verify your account."
#         )

        
# def verify_email(request, token):
#     try:
#         user_profile = UserProfile.objects.get(verification_token=token)
#         user_profile.is_email_verified = True
#         user_profile.user.is_active = True
#         user_profile.user.save()
#         print("Data pass here")
#         user_profile.save()
#         # return redirect('/login')
#         return HttpResponseRedirect(f"{settings.FRONTEND_URL}/verification-success")  # or '/login' for angular
#         # return HttpResponseRedirect(f"{settings.FRONTEND_URL}/") # for vue
#     except UserProfile.DoesNotExist:
#         return HttpResponse("Invalid verification token.", status=400)


# class LoginUser(graphene.Mutation):
#     user = graphene.Field(UserLoginObject)
#     message = graphene.String()
#     success = graphene.Boolean()

#     class Arguments:
#         input = UserLoginInputObject(required=True)

#     def mutate(self, info, input):
#         username = input.username
#         password = input.password

#         user = authenticate(username=username, password=password)

#         if user is None:
#             return LoginUser(success=False, message="Invalid username or password")

#         # Ensure user has a UserProfile
#         try:
#             user_profile = UserProfile.objects.get(user=user)
#         except UserProfile.DoesNotExist:
#             return LoginUser(success=False, message="User profile not found. Please contact support.")

#         # Check if email is verified
#         if not user_profile.is_email_verified:
#             return LoginUser(success=False, message="Email not verified. Please check your inbox for a verification link.")

#         # Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
#         return LoginUser(
#             user=UserLoginObject(
#                 id=user.id,
#                 username=user.username,
#                 email=user.email,
#                 refresh_token=str(refresh),
#                 access_token=str(refresh.access_token),
#                 isSuperuser=user.is_superuser
#             ),
#             success=True,
#             message="Login successful"
#         )













class RegistrationMutation(graphene.Mutation):
    user = graphene.Field(RegistrationObject)
    output = graphene.Field(RegistrationResponse)

    class Arguments:
        input = RegistrationInputObject(required=True)

    def mutate(self, info, input):
        response = register_user(input)

        return RegistrationMutation(user=response.user, output=response)

def verify_email(request, token):
    try:
        user_profile = UserProfile.objects.get(verification_token=token)
        user_profile.is_email_verified = True
        user_profile.user.is_active = True
        user_profile.user.save()
        print("Data pass here")
        user_profile.save()
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/verification-success")
    except UserProfile.DoesNotExist:
        return HttpResponse("Invalid verification token.", status=400)


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserLoginObject)
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        input = UserLoginInputObject(required=True)

    def mutate(self, info, input):
        username = input.username
        password = input.password

        try:
            # Authenticate user using UserBuilder
            result = UserBuilder.login_user(username, password)
            user = result["user"]

            return LoginUser(
                user=UserLoginObject(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    refresh_token=result["refresh_token"],
                    access_token=result["access_token"],
                    isSuperuser=user.is_superuser,
                ),
                success=True,
                message="Login successful",
            )

        except ValidationError as e:
            return LoginUser(success=False, message=str(e))
        except Exception:
            return LoginUser(success=False, message="An error occurred. Please try again.")



