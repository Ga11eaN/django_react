from rest_framework import serializers
from .models import ExcelFile, Sftp


class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = ('file',)


class SftpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sftp
        fields = (
            'host_name',
            'port',
            'username',
            'password',
            'key',
            'key_passphrase',
            'upload_path'
        )
