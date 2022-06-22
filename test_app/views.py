from .models import React
from .serializers import ReactSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response


class ReactViewSet(viewsets.ModelViewSet):
    queryset = React.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ReactSerializer

    def post(self, request):
        file = request.FILES['file']
        return Response(status=204)