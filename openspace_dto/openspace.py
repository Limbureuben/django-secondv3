import graphene

class RegistrationInputObject(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    passwordConfirm = graphene.String()

class RegistrationObject(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()

class LoginInputObject(graphene.InputObjectType):
    username = graphene.String()
    passoword = graphene.String()

class LoginObject(graphene.ObjectType):
    
    