import graphene
from .models import *
from django.contrib.auth.models import User
from openspaceBuilders.openspaceBuilders import *
from openspace_dto.openspace import *
from .views import RegisterUser
import graphql_jwt

class Mutation(graphene.ObjectType):
    register_users = RegisterUser.Field()

class Query(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)