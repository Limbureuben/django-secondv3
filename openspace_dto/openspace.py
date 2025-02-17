import graphene

class RegistrationInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    passwordConfirm = graphene.String()