from django.db import models


class SftpConnection(models.Model):
    host_name = models.CharField(max_length=20, default='198.19.243.251')
    port = models.IntegerField(default=2222)
    username = models.CharField(max_length=20, default='tester')
    password = models.CharField(max_length=20, default='')


class KeyUpload(models.Model):
    key_file = models.FileField()
    key_passphrase = models.CharField(max_length=20)
