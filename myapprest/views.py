from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from myapp.models import Report
from .serializers import ReportSerializer

# class FileUploadView(APIView):
#     def post(self, request):
#         file = request.FILES.get('file')
        
#         if file:
#             try:
#                 report = Report.objects.create(file=file)
#                 return Response({"Error": False, "data": ReportSerializer(report).data, "message": "File upload successfull"}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"Error": True, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         return Response({"error": True, "message": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
#     def get(self, request):
#         try:
#             data = Report.objects.all()
#             return Response(ReportSerializer(instance=data, many=True).data)
#         except Exception as e:
#             return Response({"error": True, "message": str(e)})


# from rest_framework.permissions import AllowAny

# class FileUploadView(APIView):
#     def post(self, request):
#         file = request.FILES.get('file')
#         report_id = request.data.get('report_id')  # Get report_id from request

#         if not report_id:
#             return Response({"Error": True, "message": "report_id is required"}, status=status.HTTP_400_BAD_REQUEST)

#         if file:
#             try:
#                 report, created = Report.objects.get_or_create(report_id=report_id)  # Ensure report exists
#                 report.file = file
#                 report.save()
                
#                 return Response(
#                     {"Error": False, "data": ReportSerializer(report).data, "message": "File uploaded successfully"},
#                     status=status.HTTP_200_OK
#                 )
#             except Exception as e:
#                 return Response({"Error": True, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({"Error": True, "message": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)


# views.py
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
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