import uuid
from django.conf import settings
from myapprest.models import CustomUser
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError # type: ignore
# from .tasks import send_verification_email # type: ignore
from .models import *
from openspaceBuilders.openspaceBuilders import UserBuilder, open_space, register_user, report_issue
from openspace_dto.openspace import *
from openspace_dto.Response import OpenspaceResponse, RegistrationResponse, ReportResponse
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
            # Authenticate user using the custom user model
            user = authenticate(username=username, password=password)

            if user is None:
                raise ValidationError("Invalid username or password.")

            # Ensure the user is an instance of CustomUser
            if not isinstance(user, CustomUser):
                raise ValidationError("User is not a valid CustomUser instance.")

            # Create and return tokens (assuming you use JWT or similar)
            result = UserBuilder.login_user(username, password)  # This should handle JWT generation and user data retrieval
            
            print(result)
            print(user)

            # Return user data and authentication tokens
            return LoginUser(
                user=UserLoginObject(
                    id=user.id,
                    username=user.username,
                    refresh_token=result["refresh"],
                    access_token=result["access"],
                    isStaff=user.is_staff,  # You can now access is_staff and other fields
                ),
                success=True,
                message="Login successful",
            )

        except ValidationError as e:
            return LoginUser(success=False, message=str(e))
        except Exception as e:
            return LoginUser(success=False, message=f"An error occurred: {str(e)}")

    

# class LoginUser(graphene.Mutation):
#     user = graphene.Field(UserLoginObject)
#     message = graphene.String()
#     success = graphene.Boolean()

#     class Arguments:
#         input = UserLoginInputObject(required=True)

#     def mutate(self, info, input):
#         username = input.username
#         password = input.password

#         try:
#             # Authenticate user using UserBuilder
#             result = UserBuilder.login_user(username, password)
#             print(result)
#             user = result["user"]
#             print(user)

#             # Ensure the response includes the user data and staff status
#             return LoginUser(
#                 user=UserLoginObject(
#                     id=user.id,
#                     username=user.username,
#                     refresh_token=result["refresh"],
#                     access_token=result["access"],
#                     isStaff=user.is_staff,  # Returning if the user is staff
#                 ),
#                 success=True,
#                 message="Login successful",
#             )

#         except ValidationError as e:
#             return LoginUser(success=False, message=str(e))
#         except Exception:
#             return LoginUser(success=False, message="An error occurred. Please try again.")


class RegisterUserMutation(graphene.Mutation):
    class Arguments:
        input = UserRegistrationInput(required=True)

    Output = UserRegistrationObject

    def mutate(root, info, input):
        return UserBuilder.register_user(
            username=input.username,
            password=input.password,
            passwordConfirm=input.passwordConfirm
        )

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

class ReportMutation(graphene.Mutation):
    report = graphene.Field(ReportObject)
    output = graphene.Field(ReportResponse)
    
    class Arguments:
        input = ReportInputObject(required=True)
        
    def mutate(self, info, input):
        response = report_issue(input)
        return ReportMutation(report=response.report, output=response)
    
    
class ReportType(DjangoObjectType):
    class Meta:
        model = Report
        fields = "__all__"
        
    def resolve_file_url(self, info):
        if self.file:
            return f"{settings.MEDIA_URL}{self.file}"
        return None
class CreateReport(graphene.Mutation):
    class Arguments:
        description = graphene.String(required=True)
        email = graphene.String(required=False)
        file_path = graphene.String(required=False)
        space_name = graphene.String(required=False)
        latitude = graphene.Float(required=False) 
        longitude = graphene.Float(required=False)
        user_id = graphene.ID(required=False)

    report = graphene.Field(ReportType)

    def mutate(self, info, description, email=None, file_path=None, space_name=None, latitude=None, longitude=None, user_id=None):
        user=None
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise Exception("Invalid user ID.")
        
        report = Report(
            description=description,
            email=email,
            file=file_path,
            space_name=space_name,
            latitude=latitude,
            longitude=longitude,
            user=user,
        )
        report.save()
        file_url = f"{settings.MEDIA_URL}{report.file}" if report.file else None
        return CreateReport(report=report)
    
class ReportQuery(graphene.ObjectType):
    all_reports = graphene.List(ReportType)
    
    def resolve_all_reports(self, info):
        return Report.objects.all()
    

class ConfirmReport(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()
    
    class Arguments:
        report_id = graphene.String(required=True)
        
    def mutate(self, info, report_id):
        try:
            report = Report.objects.get(report_id=report_id)
            
            ReportHistory.objects.create(
                report_id = report.report_id,
                description=report.description,
                email=report.email,
                file=report.file if report.file else None,
                user=report.user  # Link the report to the original user
            )
            
            # Delete the original report
            report.delete()
            
            # Send email if user provided one
            if report.email:
                send_mail(
                    subject="Report Confirmation",
                    message="Your report has been reviewed and confirmed.",
                    from_email="limbureubenn@gmail.com",
                    recipient_list=[report.email],
                    fail_silently=True
                )
                
            return ConfirmReport(success=True, message="Report confirmed and moved to history.")
        except Report.DoesNotExist:
            return ConfirmReport(success=False, message="Report not found.")

        
class DeleteReport(graphene.Mutation):
    message = graphene.String()
    success = graphene.String()
    
    class Arguments:
        report_id = graphene.ID(required=True)
    def mutate(self, info, report_id):
        try:
            report = Report.objects.get(pk=report_id)
            report.delete()
            return DeleteReport(success=True, message="Report deleted successfully")
        except report.DoesNotExist:
            return DeleteReport(success=False, message="Report not found")
        
class HistoryReportQuery(graphene.ObjectType):
    all_historys = graphene.List(HistoryObject)
    
    def resolve_all_historys(self, info):
        return ReportHistory.objects.all()
    
class HistoryCountQuery(graphene.ObjectType):
    total_historys = graphene.Int()
    
    def resolve_total_historys(self, info):
        return ReportHistory.objects.count()
    
class ReportCountQuery(graphene.ObjectType):
    total_report = graphene.Int()
    
    def resolve_total_report(self, info):
        return Report.objects.count()
    
class ReportAnonymousQuery(graphene.ObjectType):
    anonymous = graphene.List(HistoryObject, session_id=graphene.String(required=True))
    
    def resolve_anonymous(self, info, session_id):
        return ReportHistory.objects.filter(session_id=session_id)
    
# class AuthenticatedUserReport(graphene.ObjectType):
#     my_reports = graphene.List(HistoryObject)
    
#     def resolve_my_reports(self, info, **kwargs):
#         user = info.context.user
#         print("Authenticated user:", user)

#         if user.is_authenticated:
#             reports = ReportHistory.objects.filter(user=user)
#             print("Reports found:", reports)
#             return reports  # Make sure reports are returned!

#         print("User is anonymous or not authenticated.")  
#         return ReportHistory.objects.none()

    
    # def resolve_my_reports(self, info, **kwargs):
    #     user = info.context.user
    #     print("Authenticated user:", user)
        
    #     if user.is_authenticated:
        
    #         return ReportHistory.objects.filter(user=user)
        
    #     return ReportHistory.objects.none()
    

class AuthenticatedUserReport(graphene.ObjectType):
    my_reports = graphene.List(HistoryObject)
    
    def resolve_my_reports(self, info, **kwargs):
        user = info.context.user
        print("Authenticated user:", user)  # Debugging

        if user.is_authenticated:
            reports = UserBuilder.get_report_history(user=user)
            print(reports)  # Debugging
            return reports

        print("User is anonymous or not authenticated.")
        return ReportHistory.objects.none()


from graphql_jwt.decorators import login_required

User = get_user_model()

# class ProfileType(graphene.ObjectType):
#     id = graphene.ID()
#     username = graphene.String()
#     is_staff = graphene.Boolean()

# class UserProfileQuery(graphene.ObjectType):
#     profile = graphene.Field(ProfileType)

#     @login_required
#     def resolve_profile(self, info):
#         user = info.context.user
#         return ProfileType(
#             id=user.id,
#             username=user.username,
#             is_staff=user.is_staff
#         )

from rest_framework_simplejwt.tokens import AccessToken
# class UserProfileQuery(graphene.ObjectType):
#     profile = graphene.Field(ProfileObject)

#     @login_required
#     def resolve_profile(self, info):
#         # Extract token from context
#         request = info.context
#         auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
#         try:
#             # Extract token from Authorization header
#             token = auth_header.split('Bearer ')[1] if 'Bearer ' in auth_header else None
            
#             if not token:
#                 raise GraphQLError("No token provided")
            
#             # Decode token and extract user ID
#             decoded_token = AccessToken(token)
#             token_user_id = decoded_token.get('user_id')
            
#             # Get authenticated user
#             user = info.context.user
            
#             # Strict validation
#             if not user.is_authenticated:
#                 raise GraphQLError("User not authenticated")
            
#             # Ensure token user ID matches authenticated user
#             if user.id != token_user_id:
#                 print(f"Token User ID: {token_user_id}")
#                 print(f"Authenticated User ID: {user.id}")
#                 raise GraphQLError("Token user mismatch")
            
#             return ProfileObject(
#                 id=user.id,
#                 username=user.username,
#                 is_staff=user.is_staff
#             )
        
#         except Exception as e:
#             print(f"Profile Resolution Error: {str(e)}")
#             raise GraphQLError("Invalid authentication")


class UserProfileQuery(graphene.ObjectType):
    profile=graphene.Field(ProfileObject)
    
    def resolve_profile(self,info):
        user=info.context.user
        if user.is_authenticated:
            return UserBuilder.get_user_profile_data(user=user)
            