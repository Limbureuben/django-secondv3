import graphene
from .models import *
from django.contrib.auth.models import User

from openspace_dto import *
from openspace_dto import *
from .views import *
import graphql_jwt


class Mutation(graphene.ObjectType):
    register_users = Registration.Field()


class Query(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)