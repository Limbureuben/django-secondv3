from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.urls import path, include

# from myapp.views import verify_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', include('myapp.urls')),
    # path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
]
