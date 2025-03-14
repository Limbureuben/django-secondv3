import graphene
from  .openspace import *

class RegistrationResponse(graphene.ObjectType):
    message = graphene.String()
    success = graphene.Boolean()
    user = graphene.Field(RegistrationObject)
    
class OpenspaceResponse(graphene.ObjectType):
    message = graphene.String()
    success = graphene.Boolean()
    openspace = graphene.Field(OpenspaceObject)