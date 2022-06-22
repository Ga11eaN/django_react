from .models import React
from .serializers import ReactSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser


class ReactViewSet(viewsets.ModelViewSet):
    queryset = React.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ReactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            file_name = request.FILES['file'].name
            context = {
                'status': True,
                'message': f'Successfully uploaded file {file_name}'
            }
            return Response(context, status.HTTP_201_CREATED)
        else:
            context = {
                'status': False,
                'message': serializer.errors
            }
            return Response(context, status.HTTP_422_UNPROCESSABLE_ENTITY)
