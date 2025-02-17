from django.shortcuts import render
import graphene
from openspace.openspaceBuilders import *
from openspace.openspace_dto import *


class RegistrationMutation(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        input =  RegistrationInput(required=True)