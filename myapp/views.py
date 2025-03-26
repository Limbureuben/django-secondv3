import uuid
from django.conf import settings
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import graphene
from graphene_django import DjangoObjectType # type: ignore
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

        
# def verify_email(request, token):
#     try:
#         user_profile = UserProfile.objects.get(verification_token=token)
#         user_profile.is_email_verified = True
#         user_profile.user.is_active = True
#         user_profile.user.save()
#         print("Data pass here")
#         user_profile.save()
#         return HttpResponseRedirect(f"{settings.FRONTEND_URL}/login")
#     except UserProfile.DoesNotExist:
#         return HttpResponse("Invalid verification token.", status=400)


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

            # Ensure the response includes the user data and staff status
            return LoginUser(
                user=UserLoginObject(
                    id=user.id,
                    username=user.username,
                    refresh_token=result["refresh"],
                    access_token=result["access"],
                    isStaff=user.is_staff,  # Returning if the user is staff
                ),
                success=True,
                message="Login successful",
            )

        except ValidationError as e:
            return LoginUser(success=False, message=str(e))
        except Exception:
            return LoginUser(success=False, message="An error occurred. Please try again.")

# class RequestPasswordReset(graphene.Mutation):
#     success = graphene.Boolean()
#     message = graphene.String()

#     class Arguments:
#         email = graphene.String(required=True)

#     def mutate(self, info, email):
#         try:
#             UserBuilder.request_password_reset(email)
#             return RequestPasswordReset(success=True, message="Password reset email sent")
#         except Exception as e:
#             return RequestPasswordReset(success=False, message=str(e))
        
        
# class ResetPassword(graphene.Mutation):
#     success = graphene.Boolean()
#     message = graphene.String()

#     class Arguments:
#         token = graphene.String(required=True)
#         new_password = graphene.String(required=True)
#         password_confirm = graphene.String(required=True)

#     def mutate(self, info, token, new_password, password_confirm):
#         try:
#             UserBuilder.reset_password(token, new_password, password_confirm)
#             return ResetPassword(success=True, message="Password rest successful")
#         except ValidationError as e:
#             return ResetPassword(success=False, message=str(e))

# class ProfileQuery(graphene.ObjectType):
#     user_profile = graphene.Field(UserProfileObject, id=graphene.ID(required=True))

#     def resolve_user_profile(self, info, id):
#         try:
#             user = User.objects.get(id=id)
#             user_profile = user.userprofile
#             return UserProfileObject(
#                 id = user_profile.id,
#                 username = user.username,
#                 email = user.email
#             )
#         except User.DoesNotExist:
#             return None

# class AllUsersQuery(graphene.ObjectType):
#     all_users  = graphene.List(RegistrationObject)

#     def resolve_all_users(self, info):
#         return User.objects.all()


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
class UserProfileQuery(graphene.ObjectType):
    profile = graphene.List(ProfileObject)
    
    @login_required
    def resolve_profile(self, info):
        user = info.context.user
        return ProfileObject(username=user.username, id=user.id)
