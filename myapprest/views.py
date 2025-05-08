import os
from django.shortcuts import render
import graphene
from graphene_django import DjangoObjectType
from .utils.sms import send_confirmation_sms
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.permissions import IsAuthenticated
from .serializers import *

from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import *
from .serializers import ProblemReportSerializer
from cryptography.fernet import Fernet # type: ignore


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

        # Create a new problem report entry
        report = UssdReport.objects.create(
            phone_number=encrypted_phone,
            open_space=open_space,
            description=description,
            reference_number=reference_number,
            status="Pending"
        )

        # Serialize the response
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
