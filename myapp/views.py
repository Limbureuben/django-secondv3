from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import graphene
from .models import UserProfile
from openspaceBuilders.openspaceBuilders import register_user
from openspace_dto.openspace import *
from openspace_dto.Response import RegistrationResponse

class RegistrationMutation(graphene.Mutation):
    user = graphene.Field(RegistrationObject)
    output = graphene.Field(RegistrationResponse)

    class Arguments:
        input = RegistrationInputObject(required=True)

    def mutate(self, info, input):
        response = register_user(input)

        return RegistrationMutation(user=response.user, output=response)

def verify_email(request, token):
    try:
        user_profile = UserProfile.objects.get(verification_token=token)
        user_profile.is_email_verified = True
        user_profile.user.is_active = True
        user_profile.user.save()
        print("Data pass here")
        user_profile.save()
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/verification-success")
    except UserProfile.DoesNotExist:
        return HttpResponse("Invalid verification token.", status=400)


class LoginUser(graphene.Mutation):
    user = graphene.Field(LoginObject)
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        input = LoginInputObject(required=True)

    def mutate(self, info, input):
        username = input.username,
        password = input.password

        try:
            #authenticate the user to login
            result = UserBuilder.login_user(username, password)
            user = result['user']

         #angalia kama ni superuser
         is_superuser = user.is_superuser
        
        




