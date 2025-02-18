from django.shortcuts import render
import graphene
from openspaceBuilders.openspaceBuilders import *
from openspace_dto.openspace import *
from openspace_dto.Response import *


class RegistrationMutation(graphene.Mutation):
    user = graphene.Field(RegistrationObject)
    output = graphene.Field(RegistrationResponse)

    class Arguments:
        input =  RegistrationInputObject(required=True)

    def mutate(self, info, input):
        return  register_user(input)