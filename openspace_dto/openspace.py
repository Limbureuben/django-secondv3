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

class ReportInputObject(graphene.InputObjectType):
    description = graphene.String()
    email = graphene.String()
    district = graphene.String()
    date = graphene.String()

class ReportObject(graphene.ObjectType):
    description = graphene.String()
    email = graphene.String()
    district = graphene.String()
    date = graphene.String()
    
class OpenspaceInputObject(graphene.InputObjectType):
    name = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()
    district = graphene.String()
    
class OpenspaceObject(graphene.ObjectType):
    name = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()
    district = graphene.Float()
    