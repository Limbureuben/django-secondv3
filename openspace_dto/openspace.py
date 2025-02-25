import graphene # type: ignore
from myapp.models import *

class RegistrationInputObject(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    passwordConfirm = graphene.String()

class RegistrationObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()

class UserLoginInputObject(graphene.InputObjectType):
    username = graphene.String()
    password = graphene.String()

class UserLoginObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
    emailVerified = graphene.Boolean()
    refresh_token = graphene.String()
    access_token = graphene.String()
    isSuperuser  = graphene.Boolean()

class UserProfileObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
