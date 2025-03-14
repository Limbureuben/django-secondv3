import graphene
from .models import *
from django.contrib.auth.models import User
from openspaceBuilders.openspaceBuilders import *
from openspace_dto.openspace import *
from .views import *
import graphql_jwt

class Mutation(graphene.ObjectType):
    register_user = RegistrationMutation.Field()
    login_user =   LoginUser.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()
    add_space = CreateOpenspaceMutation.Field()

class Query(ProfileQuery,AllUsersQuery, OpenspaceQuery, graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)