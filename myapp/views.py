from django.shortcuts import render
import graphene
from openspace.openspaceBuilders import *
from openspace.openspace_dto import *


class RegistrationMutation(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        input =  RegistrationInput(required=True)