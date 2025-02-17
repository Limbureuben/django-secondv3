from django.shortcuts import render
import graphene
from openspace.openspaceBuilders.openspaceBuilders import *
from openspace.openspace_dto.openspace import *
from openspace.openspace_dto.Response import *


class RegistrationMutation(graphene.Mutation):

    output = graphene.Field(RegistrationResponse)

    class Arguments:
        input =  RegistrationInput(required=True)

    def mutate(self, info, input):
        return 