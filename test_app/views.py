from .models import ExcelFile, Sftp
from .serializers import ExcelFileSerializer, SftpSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser


class ExcelFileViewSet(viewsets.ModelViewSet):
    queryset = ExcelFile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ExcelFileSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # serializer.save()
            file_name = serializer.validated_data['file'].name
            context = {
                'status': True,
                'message': f'Successfully uploaded file {file_name}'
            }
            return Response(context, status.HTTP_201_CREATED)
        else:
            context = {
                'status': False,
                'errors': serializer.errors
            }
            return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)


class SftpViewSet(viewsets.ModelViewSet):
    queryset = Sftp.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SftpSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # serializer.save()
            file_name = serializer.validated_data['key'].name
            context = {
                'status': True,
                'message': f'Successfully validated key {file_name}'
            }
            return Response(context, status.HTTP_201_CREATED)
        else:
            context = {
                'status': False,
                'errors': serializer.errors
            }
            return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)