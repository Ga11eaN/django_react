from .models import React
from .serializers import ReactSerializer
from rest_framework import viewsets, permissions


class ReactViewSet(viewsets.ModelViewSet):
    queryset = React.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ReactSerializer