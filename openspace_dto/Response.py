import graphene

class RegistrationResponse(graphene.ObjectType):
    message = graphene.String()
    success = graphene.Boolean()