from django.contrib import admin
from .models import React
# Register your models here.


class ReactAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')


admin.site.register(React, ReactAdmin)
