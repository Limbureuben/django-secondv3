import graphene
from .models import *
from django.contrib.auth.models import User
from openspaceBuilders.openspaceBuilders import *
from openspace_dto.openspace import *
from .views import *
import graphql_jwt

class Mutation(graphene.ObjectType):
    register_user = RegistrationMutation.Field()
    # register_user = RegisterUserMutation.Field()
    login_user =   LoginUser.Field()
    register_report = ReportMutation.Field()
    create_report = CreateReport.Field()
    # request_password_reset = RequestPasswordReset.Field()
    # reset_password = ResetPassword.Field()
    add_space = CreateOpenspaceMutation.Field()
    confirm_report = ConfirmReport.Field()
    delete_report = DeleteReport.Field()
    delete_report = DeleteReport.Field()
    toggle_openspace_status = ToggleOpenspaceMutation.Field()

class Query(OpenspaceQuery, TotalOpenSpaceQuery, ReportQuery, HistoryReportQuery, HistoryCountQuery, ReportCountQuery, AnonymousReportQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)