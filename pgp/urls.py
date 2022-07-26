from rest_framework import routers
from django.urls import path
from . import views


router = routers.DefaultRouter()
router.register('sftp_connection', views.SftpConnectionViewSet, basename='sftp_connection')
router.register('key_upload', views.KeyUploadViewSet, 'key_upload')
urlpatterns = [
    path('browse_sftp', views.browse_sftp, name='browse_view')
]
urlpatterns += router.urls
