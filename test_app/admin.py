from django.contrib import admin
from .models import ExcelFile, Sftp
# Register your models here.


class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('file',)


class SftpAdmin(admin.ModelAdmin):
    pass


admin.site.register(ExcelFile, ExcelFileAdmin)
admin.site.register(Sftp, SftpAdmin)
