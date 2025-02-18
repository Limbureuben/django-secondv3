from django.http import HttpResponseRedirect
from django.shortcuts import render
import graphene
from openspaceBuilders.openspaceBuilders import *
from openspace_dto.openspace import *
from openspace_dto.Response import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

class RegistrationMutation(graphene.Mutation):
    user = graphene.Field(RegistrationObject)
    output = graphene.Field(RegistrationResponse)

    class Arguments:
        input =  RegistrationInputObject(required=True)

    def mutate(self, info, input):
        return  register_user(input)
    

def verify_email(request, token):
    try:
        user_profile = UserProfile.objects.get(verification_token=token)
        user_profile.is_email_verified = True
        user_profile.user.is_active = True
        user_profile.user.save()
        print("Data pass here")
        user_profile.save()
        # return redirect('/login')
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/verification-success")  # or '/login' for angular
        # return HttpResponseRedirect(f"{settings.FRONTEND_URL}/") # for vue
    except UserProfile.DoesNotExist:
        return HttpResponse("Invalid verification token.", status=400)


# class RegisterUser(graphene.Mutation):
#     user = graphene.Field(RegistrationObject)
#     success = graphene.Boolean()
#     message = graphene.String()
    
#     class Arguments:
#         input = RegistrationInputObject(required=True)
        
#     def mutate(self, info, input):
#         username = input.username
#         email = input.email
#         password = input.password
#         password_confirm = input.password_confirm
        
#         ##check if the user exist
#         if User.objects.filter(username=username).exists():
#             return RegisterUser(success=False, message="username alredy exists")
        
#         ##check if the email exist
#         if User.objects.filter(email=email).exists():
#             return RegisterUser(success=False, message="Email alredy exists")
        
#         if password != password_confirm:
#             return RegisterUser(success=False, message="Passwords do not match")
        
#         user = User(username=username, email=email)
#         user.set_password(password)
#         user.is_superuser = False
#         user.is_staff = False
#         user.save()
        
#         user_profile = UserProfile(user=user, verification_token=uuid.uuid4())
#         user_profile.save()
#         print("Token are created here")
        
#         # Generate verification URL
#         # verification_url = f"{settings.FRONTEND_URL}/verify-email/{user_profile.verification_token}/"
#         verification_url = f"{settings.BACKEND_URL}/verify-email/{user_profile.verification_token}/"

#         print("Token can also pass here 2")
#         # Call Celery task
#         send_verification_email.delay(email, verification_url)
        
#         return RegisterUser(
#             user=RegistrationObject(id=user.id, username=user.username, email=user.email),
#             success=True,
#             message="Registration successful. Please check your email to verify your account."
#         )

        
# def verify_email(request, token):
#     try:
#         user_profile = UserProfile.objects.get(verification_token=token)
#         user_profile.is_email_verified = True
#         user_profile.user.is_active = True
#         user_profile.user.save()
#         print("Data pass here")
#         user_profile.save()
#         # return redirect('/login')
#         return HttpResponseRedirect(f"{settings.FRONTEND_URL}/verification-success")  # or '/login' for angular
#         # return HttpResponseRedirect(f"{settings.FRONTEND_URL}/") # for vue
#     except UserProfile.DoesNotExist:
#         return HttpResponse("Invalid verification token.", status=400)
