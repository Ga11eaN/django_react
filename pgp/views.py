import os

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse

from .models import SftpConnection, KeyUpload
from .serializers import SftpConnectionSerializer, KeyUploadSerializer, BrowseSerializer
from .sftp import connect, download_file
from .file_encryption import decrypt_file


class SftpConnectionViewSet(viewsets.ModelViewSet):
    queryset = SftpConnection.objects.all()
    serializer_class = SftpConnectionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            try:
                result = connect(host_name=data['host_name'],
                                 port=data['port'],
                                 username=data['username'],
                                 password=data['password'])
                s = SessionStore()
                s['host_name'] = data['host_name']
                s['port'] = data['port']
                s['username'] = data['username']
                s['password'] = data['password']
                s['path'] = []
                s.create()
                context = {
                    'status': True,
                    'list_of_objects': result,
                    'session_key': s.session_key
                }
                my_dir = './uploads/'
                for f in os.listdir(my_dir):
                    os.remove(os.path.join(my_dir, f))
                return Response(context, status.HTTP_200_OK)
            except Exception as e:
                context = {
                    'status': False,
                    'errors': e.__str__()
                }
                return Response(context, status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                'status': False,
                'errors': serializer.errors
            }
            return Response(context, status.HTTP_404_NOT_FOUND)


class FileName:
    def __init__(self, name, obj_type, session_key):
        self.name = name
        self.obj_type = obj_type
        self.session_key = session_key


@api_view(['GET', 'POST'])
def browse_sftp(request):
    if request.method == 'GET':
        file = FileName(name='', obj_type='dir', session_key='')
        serializer = BrowseSerializer(file)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BrowseSerializer(data=request.data)
        if serializer.is_valid():
            s = SessionStore(session_key=serializer.validated_data['session_key'])
            my_path = s['path']
            if serializer.validated_data['obj_type'] == 'dir':
                if serializer.validated_data['name'] != '..':
                    my_path.append(serializer.validated_data['name'])
                else:
                    del my_path[-1]
                result = connect(host_name=s['host_name'],
                                 port=s['port'],
                                 username=s['username'],
                                 password=s['password'],
                                 dir='/'.join([item for item in my_path]))
                s['path'] = my_path
                s.save()
                context = {
                    'status': True,
                    'list_of_objects': result,
                    'path': my_path,
                    'session_key': serializer.validated_data['session_key']
                }
            else:
                my_path.append(serializer.validated_data['name'])
                s['path'] = my_path
                s.save()
                context = {
                    'status': True
                }
        else:
            context = {
                'status': False,
                'errors': serializer.errors
            }
        return Response(context, status.HTTP_200_OK)


class KeyUploadViewSet(viewsets.ModelViewSet):
    queryset = KeyUpload.objects.all()
    serializer_class = KeyUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            s = SessionStore(session_key=request.data['session_key'])
            my_path = s['path']
            # key_str = serializer.validated_data['key_file'].file.read()
            file_str = '/'.join([item for item in my_path])
            try:
                file_to_decrypt = download_file(host_name=s['host_name'],
                                                port=s['port'],
                                                username=s['username'],
                                                password=s['password'],
                                                path=file_str)
            # file = decrypt_file(key_str, file_to_decrypt, serializer.validated_data['key_passphrase'], my_path[-1][:-4])
                with open(f'./uploads/{my_path[-1]}', 'bw') as f:
                    f.write(file_to_decrypt)
                if serializer.validated_data['key_file'].name != 'test_key.txt':
                    raise ValueError("Wrong file name")
                context = {
                    'status': True,
                    'file': 'uploads/' + my_path[-1][:-4]
                }
                return Response(context, status.HTTP_200_OK)
            except Exception as ex:
                context = {
                    'status': False,
                    'file': 'uploads/' + my_path[-1][:-4],
                    'errors': ex.__str__()
                }
                return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            context = {
                'status': False,
                'errors': serializer.errors
            }
            return Response(context, status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def download_file_to_pc(request):
    if request.method == 'POST':
        s = SessionStore(session_key=request.data['session_key'])
        my_file = open(f'./uploads/{s["path"][-1]}', 'rb')
        response = HttpResponse(my_file)
        file_name = s["path"][-1]
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
