import graphene # type: ignore
from myapp.models import *

class RegistrationInputObject(graphene.InputObjectType):
    username = graphene.String()
    password = graphene.String()
    passwordConfirm = graphene.String()
    sessionId = graphene.String(required=False)

class RegistrationObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
    
class RegisterObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    
class UserRegistrationInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    passwordConfirm = graphene.String(required=True)
    
class UserRegistrationObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    access_token = graphene.String()
    refresh_token = graphene.String()

class UserLoginInputObject(graphene.InputObjectType):
    username = graphene.String()
    password = graphene.String()

class UserLoginObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    refresh_token = graphene.String()
    access_token = graphene.String()
    isStaff = graphene.Boolean()

# class UserProfileObject(graphene.ObjectType):
#     id = graphene.ID()
#     username = graphene.String()
#     email = graphene.String()

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
    id = graphene.ID()
    name = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()
    district = graphene.String()
    is_active = graphene.Boolean()
    
class ToggleOpenspaceInput(graphene.InputObjectType):
    id = graphene.ID()
    is_active = graphene.Boolean()
    
class ReportInputObject(graphene.InputObjectType):
    description = graphene.String(required=True)
    email = graphene.String(required=False)
    session_id=graphene.String(required=True)
    file_path = graphene.String(required=False)
    
class ReportObject(graphene.ObjectType):
    description = graphene.String()
    email = graphene.String()
    fileUrl = graphene.String()

class HistoryObject(graphene.ObjectType):
    reportId = graphene.String()
    description = graphene.String()
    createdAt = graphene.String()

class ProfileObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()