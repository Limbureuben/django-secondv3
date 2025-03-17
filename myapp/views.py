import uuid
from django.conf import settings
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import graphene # type: ignore
from .tasks import send_verification_email # type: ignore
from .models import *
from openspaceBuilders.openspaceBuilders import UserBuilder, open_space, register_user
from openspace_dto.openspace import *
from openspace_dto.Response import OpenspaceResponse, RegistrationResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/login")
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
                    emailVerified=result["email_verified"],
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

class RequestPasswordReset(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        try:
            UserBuilder.request_password_reset(email)
            return RequestPasswordReset(success=True, message="Password reset email sent")
        except Exception as e:
            return RequestPasswordReset(success=False, message=str(e))
        
        
class ResetPassword(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)
        password_confirm = graphene.String(required=True)

    def mutate(self, info, token, new_password, password_confirm):
        try:
            UserBuilder.reset_password(token, new_password, password_confirm)
            return ResetPassword(success=True, message="Password rest successful")
        except ValidationError as e:
            return ResetPassword(success=False, message=str(e))

class ProfileQuery(graphene.ObjectType):
    user_profile = graphene.Field(UserProfileObject, id=graphene.ID(required=True))

    def resolve_user_profile(self, info, id):
        try:
            user = User.objects.get(id=id)
            user_profile = user.userprofile
            return UserProfileObject(
                id = user_profile.id,
                username = user.username,
                email = user.email
            )
        except User.DoesNotExist:
            return None

class AllUsersQuery(graphene.ObjectType):
    all_users  = graphene.List(RegistrationObject)

    def resolve_all_users(self, info):
        return User.objects.all()












class CreateOpenspaceMutation(graphene.Mutation):
    openspace = graphene.Field(OpenspaceObject)
    output = graphene.Field(OpenspaceResponse)
    
    class Arguments:
        input = OpenspaceInputObject(required=True)
        
    def mutate(self, info, input):
        response = open_space(input)
        
        return CreateOpenspaceMutation(openspace=response.openspace, output=response)
    

class DeleteOpenspace(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()
    
    class Arguments:
        id = graphene.ID(required=True)
        
    def mutate(self, info, id):
        try:
            open_space = OpenSpace.objects.get(pk=id)
            open_space.delete()
            return DeleteOpenspace(success=True, message="Openspace delete successfully")
        except OpenSpace.DoesNotExist:
            return DeleteOpenspace(success=False, message="Fail to delete openspace")
        
        


class ToggleOpenspaceMutation(graphene.Mutation):
    class Arguments:
        input = ToggleOpenspaceInput(required=True)

    openspace = graphene.Field(OpenspaceObject)

    def mutate(self, info, input):
        try:
            openspace = OpenSpace.objects.get(pk=input.id)
            openspace.is_active = input.is_active  # Toggle the status
            openspace.save()
            return ToggleOpenspaceMutation(openspace=openspace)
        except OpenSpace.DoesNotExist:
            raise Exception("OpenSpace not found")


class OpenspaceQuery(graphene.ObjectType):
    all_open_spaces_admin = graphene.List(OpenspaceObject)
    
    all_open_spaces_user = graphene.List(OpenspaceObject)
    
    def resolve_all_open_spaces_admin(self, info):
        return OpenSpace.objects.all()
    
    def resolve_all_open_spaces_user(self, info):
        return OpenSpace.objects.filter(is_active=True)

        
class TotalOpenSpaceQuery(graphene.ObjectType):
    total_openspaces = graphene.Int()
    
    def resolve_total_openspaces(self, info):
        return OpenSpace.objects.count()
