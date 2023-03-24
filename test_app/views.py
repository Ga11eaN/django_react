from .file_generator import file_parse
from .serializers import ExcelFileSerializer, SftpSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .sftp_connection import sftp_key_upload, sftp_simple_upload
import os
from django.contrib.sessions.backends.db import SessionStore


class ExcelFileViewSet(viewsets.ModelViewSet):
    queryset = {}
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ExcelFileSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            filename = serializer.validated_data['file'].name
            excel_file = serializer.validated_data['file'].read()
            try:
                str_result = file_parse(excel_file)
                s = SessionStore()
                s['file_name'] = filename
                s.create()
                if os.path.isfile('./uploads/test.txt'):
                    os.remove('./uploads/test.txt')
                with open('./uploads/test.txt', 'w') as file:
                    file.write(str_result)
            except Exception as e:
                context = {
                    'status': False,
                    'errors': f'Wrong file format: {e.__str__()}'
                }
                return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)
            context = {
                'status': True,
                'message': f'Successfully uploaded file {filename} {os.getcwd()}',
                'session_key': s.session_key
            }
            return Response(context, status.HTTP_201_CREATED)
        else:
            context = {
                'status': False,
                'errors': serializer.errors
            }
            return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)


class SftpViewSet(viewsets.ModelViewSet):
    queryset = {}
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SftpSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            host_name = serializer.validated_data['host_name']
            port = serializer.validated_data['port']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            upload_path = serializer.validated_data['upload_path']
            ssh_check = serializer.validated_data['ssh_check']
            if ssh_check:
                key_file = serializer.validated_data['key'].read()
                key_passphrase = serializer.validated_data['key_passphrase']
            s = SessionStore(session_key=request.data['session_key'])
            filename = s['file_name']
            try:
                if ssh_check:
                    sftp_key_upload(host_name, port, username, password, key_file,
                                    upload_path, filename, key_passphrase)
                else:
                    sftp_simple_upload(host_name, port, username, password, upload_path, filename)
                if os.path.isfile('./uploads/test.txt'):
                    os.remove('./uploads/test.txt')
            except Exception as e:
                if os.path.isfile('./uploads/test.txt'):
                    os.remove('./uploads/test.txt')
                context = {
                    'status': False,
                    'errors': f'Error with sending file to SFTP server: {repr(e)}'
                }
                return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)
            context = {
                'status': True,
                'message': f'Successfully uploaded {filename}'
            }
            return Response(context, status.HTTP_201_CREATED)
        else:
            context = {
                'status': False,
                'errors': f'Error with filled data: {serializer.errors}'
            }
            return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)
