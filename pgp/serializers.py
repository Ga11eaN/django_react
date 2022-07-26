from abc import ABC

from rest_framework import serializers
from .models import SftpConnection, KeyUpload


class SftpConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SftpConnection
        fields = '__all__'


class KeyUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyUpload
        fields = '__all__'


class BrowseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    obj_type = serializers.CharField(max_length=4)
    session_key = serializers.CharField(max_length=50)
