from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class ExcelFile(models.Model):
    file = models.FileField(blank=False, validators=[FileExtensionValidator(['xlsx'])])


class Sftp(models.Model):
    host_name = models.CharField(max_length=20, blank=False)
    port = models.IntegerField(blank=False)
    username = models.CharField(max_length=20,blank=False)
    password = models.CharField(max_length=20, default='')
    key = models.FileField(validators=[FileExtensionValidator(['', 'pem'])], blank=False)
    upload_path = models.CharField(max_length=100)