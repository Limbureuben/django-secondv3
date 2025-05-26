import os
from django.shortcuts import render
import graphene
from graphene_django import DjangoObjectType

from myapprest.task import send_reset_email_task
from .utils.sms import send_confirmation_sms
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.contrib.auth.tokens import default_token_generator

from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import *
from myapp.models import *
from .serializers import ProblemReportSerializer
from cryptography.fernet import Fernet # type: ignore

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode


# views.py
from rest_framework.parsers import MultiPartParser, FormParser # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework import status # type: ignore
from django.core.files.storage import default_storage

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            # No file provided, which is okay
            return Response({'file_path': None}, status=status.HTTP_200_OK)
        
        file_path = default_storage.save(f'reports/{file_obj.name}', file_obj)
        return Response({'file_path': file_path}, status=status.HTTP_201_CREATED)
    
    
FERNET_KEY = os.getenv('FERNET_KEY')
fernet = Fernet(FERNET_KEY)

@api_view(['POST'])
def submit_problem_report(request):
    try:
        # Get data from the incoming request
        phone_number = request.data['phone_number']
        open_space = request.data['open_space']
        description = request.data['description']
        reference_number = request.data['reference_number']

        # Encrypt the phone number before saving
        encrypted_phone = fernet.encrypt(phone_number.encode()).decode()

        report = UssdReport.objects.create(
            phone_number=encrypted_phone,
            open_space=open_space,
            description=description,
            reference_number=reference_number,
            status="Pending"
        )

        serializer = ProblemReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except KeyError as e:
        return Response({'error': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def confirm_report(request, pk):
    try:
        # Get report by primary key (id)
        report = UssdReport.objects.get(pk=pk)

        # Update status
        report.status = 'Processed'
        report.save()

        # Send SMS using encrypted phone number
        success = send_confirmation_sms(report.phone_number, report.reference_number)
        if not success:
            return Response({"warning": "Report confirmed, but SMS failed to send"}, status=status.HTTP_200_OK)

        return Response({"message": "Report confirmed and SMS sent successfully."}, status=status.HTTP_200_OK)

    except UssdReport.DoesNotExist:
        return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_report_status(request, reference_number):
    try:
        # Find the report by reference number
        report = UssdReport.objects.get(reference_number=reference_number)
        serializer = ProblemReportSerializer(report)
        return Response({
            "reference_number": report.reference_number,
            "status": report.status
        }, status=status.HTTP_200_OK)
    except UssdReport.DoesNotExist:
        return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)


class UssdReportType(DjangoObjectType):
    class Meta:
        model = UssdReport

class ReportUssdQuery(graphene.ObjectType):
    all_reports_ussds = graphene.List(UssdReportType)

    def resolve_all_reports_ussds(self, info):
        # Fetch all reports
        return UssdReport.objects.all()
    


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfileImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProfileImageUploadSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            image_url = request.build_absolute_uri(serializer.data['profile_image'])
            return Response({'imageUrl': image_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)



CustomUser = get_user_model()

class SendResetPasswordEmailView(APIView):
    def post(self, request):
        print("PasswordResetRequestView POST called")

        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Use Celery to send the email asynchronously
        send_reset_email_task.delay(email, reset_link)

        return Response({'message': 'Password reset link sent to email.'}, status=200)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("password")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)

            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful"})
            else:
                return Response({"error": "Invalid token"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# class OpenSpaceBookingView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = OpenSpaceBookingSerializer(data=request.data, context={'request': request})

#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Booking successful. The open space is now unavailable."}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpenSpaceBookingView(APIView):
    def post(self, request):
        serializer = OpenSpaceBookingSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            booking = serializer.save()

            # Mark the space as unavailable
            booking.space.status = 'unavailable'
            booking.space.save()

            return Response(OpenSpaceBookingSerializer(booking).data, status=status.HTTP_201_CREATED)

        print("Booking validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DistrictBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != "ward_executive":
            return Response({"error": "Unauthorized"}, status=403)

        # Filter bookings by the district (which is equal to user's ward)
        bookings = OpenSpaceBooking.objects.filter(district=user.ward)
        serializer = OpenSpaceBookingSerializer(bookings, many=True)
        return Response(serializer.data)