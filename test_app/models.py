from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class ExcelFile(models.Model):
    file = models.FileField(blank=False, validators=[FileExtensionValidator(['xlsx'])])


class Sftp(models.Model):
    host_name = models.CharField(max_length=20, default='198.19.243.251')
    port = models.IntegerField(default=2222)
    username = models.CharField(max_length=20, default='tester')
    password = models.CharField(max_length=20, default='', blank=True)
    ssh_check = models.BooleanField(default='', blank=True)
    key = models.FileField(validators=[FileExtensionValidator(['', 'pem'])], blank=True)
    key_passphrase = models.CharField(max_length=50, default='', blank=True)
    encryption_check = models.BooleanField(default='', blank=True)
    encryption_key = models.FileField(blank=True)
    upload_path = models.CharField(max_length=100, default='/inbox/', blank=True)
